"""Orquestador de la verificación multicapa de identidad (CU-03, RF-08).

Coordina el Simulador de Identidad, las credenciales, la biometría facial,
la prueba de vida, el motor de reglas y la bitácora de auditoría para
producir un único resultado por sesión, exactamente según el flujo descrito
en el README/FD01/FD02/FD03 del proyecto.
"""

from __future__ import annotations

from datetime import datetime, timedelta
import secrets

from sqlalchemy.orm import Session

from app.models.db_models import AlertaIntentosFallidos, DesafioPruebaVida, SesionVerificacion, _now
from app.models.enums import EstadoCredencial, EstadoSesion
from app.models.enums import ResultadoVerificacion as R
from app.services.auditoria_service import AuditoriaService
from app.services.biometria_service import BiometriaService
from app.services.credencial_service import CredencialService
from app.services.errors import (
    CredencialNoRegistradaError,
    DesafioPruebaVidaAccionInvalidaError,
    DesafioPruebaVidaAgotadoError,
    DesafioPruebaVidaRequeridoError,
    IdentidadTemporalmenteBloqueadaError,
    SesionNoEncontradaError,
    SesionNoVigenteError,
)
from app.services.identidad_service import IdentidadService
from app.services.liveness_service import LivenessService
from app.services.reglas_service import ReglasService

VIGENCIA_SESION = timedelta(minutes=10)
INTENTOS_FALLIDOS_MAXIMOS = 3
BLOQUEO_TEMPORAL = timedelta(minutes=15)
DURACION_DESAFIO_VIDA = timedelta(seconds=20)
REINTENTOS_DESAFIO_VIDA_MAXIMOS = 1
ACCIONES_PRUEBA_VIDA = ("PARPADEO", "GIRO_IZQUIERDA", "GIRO_DERECHA")


class VerificacionService:
    def __init__(self, db: Session):
        self.db = db
        self.credenciales = CredencialService(db)
        self.identidades = IdentidadService(db)
        self.biometria = BiometriaService()
        self.liveness = LivenessService()
        self.reglas = ReglasService()
        self.auditoria = AuditoriaService(db)

    # ------------------------------------------------------------------
    # CU-03, paso 1-2: lectura de credencial e identificación del registro
    # ------------------------------------------------------------------
    def iniciar_sesion(
        self, codigo_credencial: str, id_responsable: str | None
    ) -> SesionVerificacion:
        credencial = None
        id_identidad = None
        id_credencial = None
        try:
            credencial = self.credenciales.leer(codigo_credencial)
            id_identidad = credencial.id_identidad
            id_credencial = credencial.id
            self._comprobar_bloqueo_temporal(id_identidad)
        except CredencialNoRegistradaError:
            pass

        sesion = SesionVerificacion(
            id_identidad=id_identidad,
            id_credencial=id_credencial,
            id_responsable=id_responsable,
            estado=EstadoSesion.EN_CURSO,
        )
        self.db.add(sesion)
        self.db.commit()
        self.db.refresh(sesion)

        self.auditoria.registrar_evento(
            sesion.id, "SESION_INICIADA", {"codigo_credencial": codigo_credencial}
        )

        if credencial is None:
            self._finalizar_con_resultado(sesion, R.CREDENCIAL_NO_REGISTRADA)
        elif credencial.estado == EstadoCredencial.REVOCADA:
            self._finalizar_con_resultado(sesion, R.CREDENCIAL_REVOCADA)

        return sesion

    def _comprobar_bloqueo_temporal(self, id_identidad: str) -> None:
        alerta = (
            self.db.query(AlertaIntentosFallidos)
            .filter(AlertaIntentosFallidos.id_identidad == id_identidad)
            .filter(AlertaIntentosFallidos.fecha_resolucion.is_(None))
            .order_by(AlertaIntentosFallidos.fecha_creacion.desc())
            .first()
        )
        if alerta is None:
            return
        if alerta.bloqueada_hasta <= _now():
            alerta.fecha_resolucion = _now()
            self.db.commit()
            self.auditoria.registrar_evento(None, "BLOQUEO_TEMPORAL_VENCIDO", {"id_identidad": id_identidad})
            return
        raise IdentidadTemporalmenteBloqueadaError(
            f"La identidad está bloqueada temporalmente hasta {alerta.bloqueada_hasta.isoformat()}."
        )

    def listar_alertas(self) -> list[AlertaIntentosFallidos]:
        self._resolver_alertas_vencidas()
        return self.db.query(AlertaIntentosFallidos).order_by(AlertaIntentosFallidos.fecha_creacion.desc()).all()

    def resolver_alerta(self, id_alerta: str, id_administrador: str) -> AlertaIntentosFallidos:
        alerta = self.db.get(AlertaIntentosFallidos, id_alerta)
        if alerta is None:
            raise SesionNoEncontradaError(f"No existe la alerta '{id_alerta}'.")
        if alerta.fecha_resolucion is None:
            alerta.fecha_resolucion = _now()
            alerta.resuelta_por = id_administrador
            self.db.commit()
            self.auditoria.registrar_evento(None, "BLOQUEO_TEMPORAL_REACTIVADO", {"id_identidad": alerta.id_identidad, "id_alerta": alerta.id, "id_administrador": id_administrador})
        return alerta

    def _resolver_alertas_vencidas(self) -> None:
        alertas = self.db.query(AlertaIntentosFallidos).filter(AlertaIntentosFallidos.fecha_resolucion.is_(None)).filter(AlertaIntentosFallidos.bloqueada_hasta <= _now()).all()
        for alerta in alertas:
            alerta.fecha_resolucion = _now()
        if alertas:
            self.db.commit()

    def _obtener_sesion_vigente(self, id_sesion: str) -> SesionVerificacion:
        sesion = self.db.get(SesionVerificacion, id_sesion)
        if sesion is None:
            raise SesionNoEncontradaError(f"No existe la sesión '{id_sesion}'.")
        if sesion.estado != EstadoSesion.EN_CURSO:
            raise SesionNoVigenteError(
                f"La sesión '{id_sesion}' ya no está en curso (estado: {sesion.estado})."
            )
        if _now() - sesion.fecha_inicio > VIGENCIA_SESION:
            sesion.estado = EstadoSesion.EXPIRADA
            self.db.commit()
            self.auditoria.registrar_evento(sesion.id, "SESION_EXPIRADA", {})
            raise SesionNoVigenteError(f"La sesión '{id_sesion}' expiró por inactividad (RN-10).")
        return sesion

    def expirar_sesiones_vencidas(self) -> int:
        """Materializa la expiración al operar/consultar, sin tarea en segundo plano."""
        limite = _now() - VIGENCIA_SESION
        vencidas = (
            self.db.query(SesionVerificacion)
            .filter(SesionVerificacion.estado == EstadoSesion.EN_CURSO)
            .filter(SesionVerificacion.fecha_inicio < limite)
            .all()
        )
        for sesion in vencidas:
            sesion.estado = EstadoSesion.EXPIRADA
            sesion.fecha_fin = _now()
        if vencidas:
            self.db.commit()
            for sesion in vencidas:
                self.auditoria.registrar_evento(sesion.id, "SESION_EXPIRADA", {"origen": "consulta"})
        return len(vencidas)

    def listar_sesiones(
        self,
        resultado: str | None = None,
        fecha_desde: datetime | None = None,
        fecha_hasta: datetime | None = None,
        id_identidad: str | None = None,
    ) -> list[SesionVerificacion]:
        self.expirar_sesiones_vencidas()
        query = self.db.query(SesionVerificacion)
        if resultado:
            query = query.filter(SesionVerificacion.resultado == resultado)
        if fecha_desde:
            query = query.filter(SesionVerificacion.fecha_inicio >= fecha_desde)
        if fecha_hasta:
            query = query.filter(SesionVerificacion.fecha_inicio <= fecha_hasta)
        if id_identidad:
            query = query.filter(SesionVerificacion.id_identidad == id_identidad)
        return query.order_by(SesionVerificacion.fecha_inicio.desc()).all()

    # ------------------------------------------------------------------
    # CU-03, paso 3-4: captura y comparación facial
    # ------------------------------------------------------------------
    def registrar_captura_facial(self, id_sesion: str, imagen_bytes: bytes) -> SesionVerificacion:
        sesion = self._obtener_sesion_vigente(id_sesion)
        referencia = self.identidades.referencia_facial_bytes(sesion.id_identidad)
        coincide, confianza = self.biometria.comparar_rostro(referencia, imagen_bytes)

        sesion.rostro_coincide = coincide
        sesion.confianza_facial = confianza
        self.db.commit()
        self.db.refresh(sesion)

        self.auditoria.registrar_evento(
            sesion.id, "ROSTRO_EVALUADO", {"coincide": coincide, "confianza": confianza}
        )

        if not coincide:
            self._finalizar_con_resultado(sesion, R.ROSTRO_NO_COINCIDENTE)
        return sesion

    # ------------------------------------------------------------------
    # CU-03, paso 5-9: desafío y prueba de vida, reglas y resultado final
    # ------------------------------------------------------------------
    def emitir_desafio_prueba_vida(self, id_sesion: str) -> DesafioPruebaVida:
        """Emite un desafío breve y permite una sola repetición trazable."""
        sesion = self._obtener_sesion_vigente(id_sesion)
        if sesion.rostro_coincide is not True:
            raise ValueError("La comparación facial debe aprobarse antes de la prueba de vida.")

        desafio = self.db.query(DesafioPruebaVida).filter_by(id_sesion=sesion.id).one_or_none()
        ahora = _now()
        reemplazo = desafio is not None
        if desafio is not None and desafio.estado == "PENDIENTE":
            if desafio.fecha_vencimiento <= ahora:
                self._vencer_desafio(sesion, desafio)
                raise DesafioPruebaVidaRequeridoError("El desafío de vida venció; inicie una nueva verificación.")
            if desafio.reintentos >= REINTENTOS_DESAFIO_VIDA_MAXIMOS:
                raise DesafioPruebaVidaAgotadoError(
                    "El desafío actual ya consumió la única repetición permitida."
                )
            opciones = [accion for accion in ACCIONES_PRUEBA_VIDA if accion != desafio.accion]
            desafio.accion = secrets.choice(opciones)
            desafio.reintentos += 1
        elif desafio is None:
            desafio = DesafioPruebaVida(
                id_sesion=sesion.id,
                accion=secrets.choice(ACCIONES_PRUEBA_VIDA),
                fecha_vencimiento=ahora + DURACION_DESAFIO_VIDA,
            )
            self.db.add(desafio)
        else:
            raise DesafioPruebaVidaRequeridoError(
                "El desafío anterior ya fue resuelto; inicie una nueva verificación."
            )

        desafio.estado = "PENDIENTE"
        desafio.fecha_emision = ahora
        desafio.fecha_vencimiento = ahora + DURACION_DESAFIO_VIDA
        self.db.commit()
        self.db.refresh(desafio)
        self.auditoria.registrar_evento(
            sesion.id,
            "DESAFIO_PRUEBA_DE_VIDA_REEMPLAZADO" if reemplazo else "DESAFIO_PRUEBA_DE_VIDA_EMITIDO",
            {
                "accion": desafio.accion,
                "fecha_vencimiento": desafio.fecha_vencimiento.isoformat(),
                "reintentos": desafio.reintentos,
                "experimental": True,
            },
        )
        return desafio

    def _vencer_desafio(self, sesion: SesionVerificacion, desafio: DesafioPruebaVida) -> None:
        desafio.estado = "VENCIDO"
        desafio.fecha_resolucion = _now()
        self.db.commit()
        self.auditoria.registrar_evento(
            sesion.id,
            "PRUEBA_DE_VIDA_VENCIDA",
            {
                "accion": desafio.accion,
                "fecha_vencimiento": desafio.fecha_vencimiento.isoformat(),
                "motivo": "TIEMPO_AGOTADO",
                "experimental": True,
            },
        )
        self._finalizar_con_resultado(sesion, R.PRUEBA_DE_VIDA_FALLIDA)

    def registrar_prueba_vida(
        self, id_sesion: str, imagen_bytes: bytes, accion: str | None = None
    ) -> SesionVerificacion:
        sesion = self._obtener_sesion_vigente(id_sesion)
        desafio = self.db.query(DesafioPruebaVida).filter_by(id_sesion=sesion.id).one_or_none()
        if desafio is None or desafio.estado != "PENDIENTE":
            raise DesafioPruebaVidaRequeridoError(
                "Solicite un desafío de vida vigente antes de enviar una captura."
            )
        if desafio.fecha_vencimiento <= _now():
            self._vencer_desafio(sesion, desafio)
            return sesion
        if accion is not None and accion != desafio.accion:
            raise DesafioPruebaVidaAccionInvalidaError(
                "La acción enviada no coincide con el desafío de vida vigente."
            )

        superado, detalle = self.liveness.validar_accion(desafio.accion, imagen_bytes)

        sesion.prueba_vida_accion = desafio.accion
        sesion.prueba_vida_superada = superado
        desafio.estado = "RESUELTO"
        desafio.fecha_resolucion = _now()
        self.db.commit()
        self.db.refresh(sesion)

        self.auditoria.registrar_evento(
            sesion.id,
            "PRUEBA_DE_VIDA_EVALUADA",
            {
                "accion": desafio.accion,
                "superado": superado,
                "fecha_vencimiento": desafio.fecha_vencimiento.isoformat(),
                **detalle,
            },
        )

        resultado = self.reglas.evaluar(
            credencial_registrada=True,
            credencial_revocada=False,
            rostro_coincide=sesion.rostro_coincide,
            prueba_vida_superada=superado,
        )
        self._finalizar_con_resultado(sesion, resultado)
        return sesion

    # ------------------------------------------------------------------
    # Cierre de sesión, bitácora y bloqueo por intentos fallidos (RN-05)
    # ------------------------------------------------------------------
    def _finalizar_con_resultado(self, sesion: SesionVerificacion, resultado: str) -> None:
        sesion.resultado = resultado
        sesion.estado = EstadoSesion.COMPLETADA
        sesion.fecha_fin = _now()
        self.db.commit()
        self.db.refresh(sesion)

        self.auditoria.registrar_evento(sesion.id, "SESION_FINALIZADA", {"resultado": resultado})

        if resultado != R.IDENTIDAD_VERIFICADA and sesion.id_identidad:
            self._evaluar_intentos_fallidos(sesion.id_identidad)

    def _evaluar_intentos_fallidos(self, id_identidad: str) -> None:
        ultimas = (
            self.db.query(SesionVerificacion)
            .filter(SesionVerificacion.id_identidad == id_identidad)
            .filter(SesionVerificacion.estado == EstadoSesion.COMPLETADA)
            .order_by(SesionVerificacion.fecha_fin.desc())
            .limit(INTENTOS_FALLIDOS_MAXIMOS)
            .all()
        )
        if len(ultimas) < INTENTOS_FALLIDOS_MAXIMOS:
            return
        if all(s.resultado != R.IDENTIDAD_VERIFICADA for s in ultimas):
            alerta = AlertaIntentosFallidos(
                id_identidad=id_identidad,
                intentos_consecutivos=INTENTOS_FALLIDOS_MAXIMOS,
                bloqueada_hasta=_now() + BLOQUEO_TEMPORAL,
            )
            self.db.add(alerta)
            self.db.commit()
            self.auditoria.registrar_evento(
                None,
                "ALERTA_INTENTOS_FALLIDOS",
                {
                    "id_identidad": id_identidad,
                    "intentos_consecutivos": INTENTOS_FALLIDOS_MAXIMOS,
                    "bloqueada_hasta": alerta.bloqueada_hasta,
                },
            )
