"""Simulador SID-Sunarp (RF-13, RF-14, RN-06).

Representa, únicamente para fines académicos, el envío de un trámite
ficticio a un servicio institucional externo equivalente al SID-Sunarp
real. No reproduce sus procedimientos oficiales.
"""

from __future__ import annotations

from time import perf_counter

from sqlalchemy.orm import Session

from app.models import schemas
from app.models.db_models import DocumentoVerificado, EvidenciaTramite, SesionVerificacion, TramiteSimulado
from app.models.enums import EstadoTramite
from app.models.enums import ResultadoVerificacion as R
from app.services.documento_service import DocumentoService
from app.services.errors import (
    DocumentoIntegridadInvalidaError,
    DocumentoNoEncontradoError,
    EvidenciaTramiteNoEncontradaError,
    SesionNoEncontradaError,
    TramiteNoHabilitadoError,
)
from app.services.auditoria_service import AuditoriaService

_ESTADOS_POR_ESCENARIO = {
    "DISPONIBLE": EstadoTramite.ENVIADO,
    "RECHAZADO": EstadoTramite.RECHAZADO,
    "SERVICIO_NO_DISPONIBLE": EstadoTramite.ERROR_SERVICIO,
    "TIEMPO_AGOTADO": EstadoTramite.TIEMPO_AGOTADO,
    "RESPUESTA_INVALIDA": EstadoTramite.RESPUESTA_INVALIDA,
    "ERROR_INTERNO": EstadoTramite.ERROR_INTERNO,
}


class SidSunarpSimuladoService:
    def __init__(self, db: Session):
        self.db = db

    def enviar_tramite(
        self, id_sesion: str, id_documento: str, escenario: str = "DISPONIBLE"
    ) -> TramiteSimulado:
        sesion = self.db.get(SesionVerificacion, id_sesion)
        if sesion is None:
            raise SesionNoEncontradaError(f"No existe la sesión '{id_sesion}'.")
        if sesion.resultado != R.IDENTIDAD_VERIFICADA:
            raise TramiteNoHabilitadoError(
                "Solo se puede enviar un trámite si la sesión tiene resultado "
                "IDENTIDAD_VERIFICADA (RN-06)."
            )

        documento = self.db.get(DocumentoVerificado, id_documento)
        if documento is None:
            raise DocumentoNoEncontradoError(f"No existe el documento '{id_documento}'.")
        if documento.id_sesion != id_sesion:
            raise TramiteNoHabilitadoError(
                "El documento debe pertenecer a la sesión que habilita el trámite."
            )
        if not DocumentoService.integridad_vigente(documento):
            raise DocumentoIntegridadInvalidaError(
                "La integridad vigente del documento es obligatoria para el trámite (RN-08)."
            )

        if escenario not in _ESTADOS_POR_ESCENARIO:
            raise ValueError("Escenario SID no soportado.")
        inicio = perf_counter()
        estado = _ESTADOS_POR_ESCENARIO[escenario]

        tramite = TramiteSimulado(id_sesion=id_sesion, estado=estado)
        self.db.add(tramite)
        self.db.flush()
        evidencia = EvidenciaTramite(
            id_sesion=id_sesion, id_documento=id_documento, id_tramite=tramite.id
        )
        self.db.add(evidencia)
        self.db.commit()
        self.db.refresh(tramite)
        AuditoriaService(self.db).registrar_evento(id_sesion, "EVIDENCIA_TRAMITE_ASOCIADA", {
            "id_documento": id_documento,
            "id_tramite": tramite.id,
            "resultado_sesion": sesion.resultado,
        })
        AuditoriaService(self.db).registrar_evento(id_sesion, "TRAMITE_SIMULADO_EVALUADO", {
            "id_documento": id_documento,
            "id_tramite": tramite.id,
            "escenario": escenario, "estado": estado,
            "duracion_ms": round((perf_counter() - inicio) * 1000, 3),
            "respuesta_minima": "TRAMITE_SIMULADO",
        })
        return tramite

    def obtener_evidencia(self, id_tramite: str) -> schemas.EvidenciaTramiteRespuesta:
        evidencia = self.db.query(EvidenciaTramite).filter_by(id_tramite=id_tramite).first()
        if evidencia is None:
            raise EvidenciaTramiteNoEncontradaError(
                f"No existe evidencia para el trámite '{id_tramite}'."
            )
        sesion = self.db.get(SesionVerificacion, evidencia.id_sesion)
        documento = self.db.get(DocumentoVerificado, evidencia.id_documento)
        tramite = self.db.get(TramiteSimulado, evidencia.id_tramite)
        if sesion is None or documento is None or tramite is None:
            raise EvidenciaTramiteNoEncontradaError("La evidencia no se puede reconstruir.")
        return schemas.EvidenciaTramiteRespuesta(
            id_tramite=tramite.id,
            id_sesion=sesion.id,
            id_documento=documento.id,
            resultado_sesion=sesion.resultado,
            estado_tramite=tramite.estado,
            integridad_documento=(
                "INTEGRO" if DocumentoService.integridad_vigente(documento)
                else "INTEGRIDAD_NO_VERIFICADA"
            ),
            fecha_tramite=tramite.fecha,
        )
