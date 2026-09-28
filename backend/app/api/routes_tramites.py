"""Endpoints del Simulador SID-Sunarp (RF-13, RF-14, RN-06)."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import schemas
from app.services.sid_sunarp_service import SidSunarpSimuladoService

router = APIRouter(prefix="/tramites", tags=["Simulador SID-Sunarp"])


@router.post("", response_model=schemas.TramiteRespuesta, status_code=201)
def enviar_tramite(id_sesion: str, escenario: str = "DISPONIBLE", db: Session = Depends(get_db)):
    return SidSunarpSimuladoService(db).enviar_tramite(id_sesion, escenario)
