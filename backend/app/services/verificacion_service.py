"""Orquestador de la verificación multicapa de identidad (CU-03, RF-08).

Coordina el Simulador de Identidad, las credenciales, la biometría facial,
la prueba de vida, el motor de reglas y la bitácora de auditoría para
producir un único resultado por sesión, exactamente según el flujo descrito
en el README/FD01/FD02/FD03 del proyecto.
"""

from __future__ import annotations

from datetime import timedelta

from sqlalchemy.orm import Session

from app.models.db_models import SesionVerificacion, _now
from app.models.enums import EstadoCredencial, EstadoSesion
from app.models.enums import ResultadoVerificacion as R
from app.services.auditoria_service import AuditoriaService
from app.services.biometria_service import BiometriaService
from app.services.credencial_service import CredencialService
from app.services.errors import (
    CredencialNoRegistradaError,
    SesionNoEncontradaError,
    SesionNoVigenteError,
)
from app.services.identidad_service import IdentidadService
from app.services.liveness_service import LivenessService
from app.services.reglas_service import ReglasService

VIGENCIA_SESION = timedelta(minutes=10)
INTENTOS_FALLIDOS_MAXIMOS = 3


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
    # CU-03, paso 5-9: prueba de vida, motor de reglas y resultado final
    # ------------------------------------------------------------------
    def registrar_prueba_vida(
        self, id_sesion: str, accion: str, imagen_bytes: bytes
    ) -> SesionVerificacion:
        sesion = self._obtener_sesion_vigente(id_sesion)
        superado, detalle = self.liveness.validar_accion(accion, imagen_bytes)

        sesion.prueba_vida_accion = accion
        sesion.prueba_vida_superada = superado
        self.db.commit()
        self.db.refresh(sesion)

        self.auditoria.registrar_evento(
            sesion.id,
            "PRUEBA_DE_VIDA_EVALUADA",
            {"accion": accion, "superado": superado, **detalle},
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
            self.identidades.bloquear(id_identidad)
            self.auditoria.registrar_evento(
                None,
                "ALERTA_INTENTOS_FALLIDOS",
                {
                    "id_identidad": id_identidad,
                    "intentos_consecutivos": INTENTOS_FALLIDOS_MAXIMOS,
                },
            )
