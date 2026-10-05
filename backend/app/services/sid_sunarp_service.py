"""Simulador SID-Sunarp (RF-13, RF-14, RN-06).

Representa, únicamente para fines académicos, el envío de un trámite
ficticio a un servicio institucional externo equivalente al SID-Sunarp
real. No reproduce sus procedimientos oficiales.
"""

from __future__ import annotations

from time import perf_counter

from sqlalchemy.orm import Session

from app.models.db_models import SesionVerificacion, TramiteSimulado
from app.models.enums import EstadoTramite
from app.models.enums import ResultadoVerificacion as R
from app.services.errors import SesionNoEncontradaError, TramiteNoHabilitadoError
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

    def enviar_tramite(self, id_sesion: str, escenario: str = "DISPONIBLE") -> TramiteSimulado:
        sesion = self.db.get(SesionVerificacion, id_sesion)
        if sesion is None:
            raise SesionNoEncontradaError(f"No existe la sesión '{id_sesion}'.")
        if sesion.resultado != R.IDENTIDAD_VERIFICADA:
            raise TramiteNoHabilitadoError(
                "Solo se puede enviar un trámite si la sesión tiene resultado "
                "IDENTIDAD_VERIFICADA (RN-06)."
            )

        if escenario not in _ESTADOS_POR_ESCENARIO:
            raise ValueError("Escenario SID no soportado.")
        inicio = perf_counter()
        estado = _ESTADOS_POR_ESCENARIO[escenario]

        tramite = TramiteSimulado(id_sesion=id_sesion, estado=estado)
        self.db.add(tramite)
        self.db.commit()
        self.db.refresh(tramite)
        AuditoriaService(self.db).registrar_evento(id_sesion, "TRAMITE_SIMULADO_EVALUADO", {
            "escenario": escenario, "estado": estado,
            "duracion_ms": round((perf_counter() - inicio) * 1000, 3),
            "respuesta_minima": "TRAMITE_SIMULADO",
        })
        return tramite
