"""Endpoints del Simulador SID-Sunarp (RF-13, RF-14, RN-06)."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth import require_roles
from app.core.database import get_db
from app.models import schemas
from app.models.enums import RolUsuario
from app.services.sid_sunarp_service import SidSunarpSimuladoService

router = APIRouter(prefix="/tramites", tags=["Simulador SID-Sunarp"])


@router.post("", response_model=schemas.TramiteRespuesta, status_code=201)
def enviar_tramite(
    id_sesion: str,
    id_documento: str,
    escenario: str = "DISPONIBLE",
    db: Session = Depends(get_db),
    _=Depends(require_roles(RolUsuario.OPERADOR, RolUsuario.ADMINISTRADOR)),
):
    return SidSunarpSimuladoService(db).enviar_tramite(id_sesion, id_documento, escenario)


@router.get("/{id_tramite}/evidencia", response_model=schemas.EvidenciaTramiteRespuesta)
def consultar_evidencia(
    id_tramite: str,
    db: Session = Depends(get_db),
    _=Depends(require_roles(RolUsuario.ADMINISTRADOR, RolUsuario.AUDITOR)),
):
    return SidSunarpSimuladoService(db).obtener_evidencia(id_tramite)
