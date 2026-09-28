"""Endpoints de credenciales de prueba QR/RFID (RF-03, RF-04, RN-04)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.auth import require_roles
from app.models.enums import RolUsuario
from app.models import schemas
from app.services.credencial_service import CredencialService

router = APIRouter(
    prefix="/credenciales", tags=["Credenciales QR/RFID"],
    dependencies=[Depends(require_roles(RolUsuario.ADMINISTRADOR))],
)


@router.post("", response_model=schemas.CredencialRespuesta, status_code=201)
def emitir_credencial(datos: schemas.CredencialCrear, db: Session = Depends(get_db)):
    return CredencialService(db).emitir(datos)


@router.get("", response_model=list[schemas.CredencialRespuesta])
def listar_credenciales(db: Session = Depends(get_db)):
    """Todas las credenciales emitidas, con su estado actual (RF-18)."""
    return CredencialService(db).listar()


@router.get("/rfid/{uid}", response_model=schemas.CredencialRespuesta)
def leer_rfid_simulado(uid: str, db: Session = Depends(get_db)):
    """Lectura del adaptador RFID simulado; nunca aprueba una verificación."""
    return CredencialService(db).leer_rfid(uid)


@router.get("/{codigo}", response_model=schemas.CredencialRespuesta)
def leer_credencial(codigo: str, db: Session = Depends(get_db)):
    return CredencialService(db).leer(codigo)


@router.post("/{id_credencial}/revocar", response_model=schemas.CredencialRespuesta)
def revocar_credencial(id_credencial: str, db: Session = Depends(get_db)):
    return CredencialService(db).revocar(id_credencial)


@router.get("/{codigo}/qr")
def obtener_imagen_qr(codigo: str, db: Session = Depends(get_db)):
    servicio = CredencialService(db)
    credencial = servicio.leer(codigo)
    imagen = servicio.generar_imagen_qr(credencial)
    return Response(content=imagen, media_type="image/png")
