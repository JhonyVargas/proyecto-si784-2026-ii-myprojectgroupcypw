"""Simulador SID-Sunarp (RF-13, RF-14, RN-06).

Representa, únicamente para fines académicos, el envío de un trámite
ficticio a un servicio institucional externo equivalente al SID-Sunarp
real. No reproduce sus procedimientos oficiales.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.db_models import SesionVerificacion, TramiteSimulado
from app.models.enums import EstadoTramite
from app.models.enums import ResultadoVerificacion as R
from app.services.errors import SesionNoEncontradaError, TramiteNoHabilitadoError

_ESTADOS_POR_ESCENARIO = {
    "DISPONIBLE": EstadoTramite.ENVIADO,
    "RECHAZADO": EstadoTramite.RECHAZADO,
    "SERVICIO_NO_DISPONIBLE": EstadoTramite.ERROR_SERVICIO,
    "TIEMPO_AGOTADO": EstadoTramite.TIEMPO_AGOTADO,
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

        estado = _ESTADOS_POR_ESCENARIO.get(escenario, EstadoTramite.ERROR_SERVICIO)

        tramite = TramiteSimulado(id_sesion=id_sesion, estado=estado)
        self.db.add(tramite)
        self.db.commit()
        self.db.refresh(tramite)
        return tramite
