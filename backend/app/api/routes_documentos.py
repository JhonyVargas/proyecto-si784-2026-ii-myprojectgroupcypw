"""Endpoints de integridad documental (RF-09, RF-10, RN-08)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import schemas
from app.services.documento_service import DocumentoService
from app.services.errors import DocumentoNoEncontradoError

router = APIRouter(prefix="/documentos", tags=["Integridad documental"])


@router.post("", response_model=schemas.DocumentoRespuesta, status_code=201)
def generar_documento(id_sesion: str, contenido: str, db: Session = Depends(get_db)):
    return DocumentoService(db).generar_documento(id_sesion, contenido)


@router.post("/{id_documento}/verificar", response_model=schemas.IntegridadDocumentoRespuesta)
def verificar_integridad(
    id_documento: str, archivo: UploadFile = File(...), db: Session = Depends(get_db)
):
    try:
        contenido_actual = archivo.file.read()
        return DocumentoService(db).verificar_integridad(id_documento, contenido_actual)
    except DocumentoNoEncontradoError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
