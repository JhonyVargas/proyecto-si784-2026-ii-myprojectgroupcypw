"""Endpoints del flujo de verificación multicapa (CU-03, RF-05 a RF-08)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import schemas
from app.services.errors import (
    RostroNoDetectadoError,
    SesionNoEncontradaError,
    SesionNoVigenteError,
)
from app.services.verificacion_service import VerificacionService

router = APIRouter(prefix="/verificaciones", tags=["Verificación multicapa"])


@router.post("", response_model=schemas.SesionRespuesta, status_code=201)
def iniciar_verificacion(datos: schemas.SesionIniciar, db: Session = Depends(get_db)):
    return VerificacionService(db).iniciar_sesion(datos.codigo_credencial, datos.id_responsable)


@router.post("/{id_sesion}/rostro", response_model=schemas.SesionRespuesta)
def capturar_rostro(
    id_sesion: str, imagen: UploadFile = File(...), db: Session = Depends(get_db)
):
    try:
        imagen_bytes = imagen.file.read()
        return VerificacionService(db).registrar_captura_facial(id_sesion, imagen_bytes)
    except SesionNoEncontradaError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except SesionNoVigenteError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except RostroNoDetectadoError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/{id_sesion}/prueba-vida", response_model=schemas.SesionRespuesta)
def ejecutar_prueba_vida(
    id_sesion: str,
    accion: str,
    imagen: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        imagen_bytes = imagen.file.read()
        return VerificacionService(db).registrar_prueba_vida(id_sesion, accion, imagen_bytes)
    except SesionNoEncontradaError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except SesionNoVigenteError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except RostroNoDetectadoError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
