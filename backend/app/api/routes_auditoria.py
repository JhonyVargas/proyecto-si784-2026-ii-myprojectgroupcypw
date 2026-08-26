"""Endpoints de la bitácora de auditoría (RF-11, RF-12, RF-17)."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import schemas
from app.services.auditoria_service import AuditoriaService

router = APIRouter(prefix="/auditoria", tags=["Bitácora de auditoría"])


@router.get("/eventos", response_model=list[schemas.EventoAuditoriaRespuesta])
def listar_eventos(id_sesion: Optional[str] = None, db: Session = Depends(get_db)):
    return AuditoriaService(db).listar_eventos(id_sesion)


@router.get("/verificar-cadena", response_model=schemas.VerificacionCadenaRespuesta)
def verificar_cadena(db: Session = Depends(get_db)):
    return AuditoriaService(db).verificar_cadena()
