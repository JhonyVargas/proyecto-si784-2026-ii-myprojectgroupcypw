"""Endpoints de integridad documental (RF-09, RF-10, RN-08)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.api.auth import require_roles
from app.core.database import get_db
from app.core.seguridad import leer_carga
from app.models import schemas
from app.models.enums import RolUsuario
from app.services.documento_service import DocumentoService

router = APIRouter(prefix="/documentos", tags=["Integridad documental"])


@router.get("/consulta/{identificador}", response_model=schemas.ConsultaDocumentoRespuesta)
def consultar_qr_documental(identificador: str, db: Session = Depends(get_db)):
    """Contrato público del QR documental, separado de credenciales QR."""
    return DocumentoService(db).consultar_qr(identificador)


MAX_CONTENIDO_DOCUMENTO = 20_000


@router.post("", response_model=schemas.DocumentoRespuesta, status_code=201)
def generar_documento(
    id_sesion: str,
    contenido: str = Form(..., min_length=1, max_length=MAX_CONTENIDO_DOCUMENTO),
    db: Session = Depends(get_db),
    _=Depends(require_roles(RolUsuario.OPERADOR, RolUsuario.ADMINISTRADOR)),
):
    """El contenido viaja en el cuerpo para no quedar en URLs ni logs de acceso (#22)."""
    return DocumentoService(db).generar_documento(id_sesion, contenido)


@router.post("/{id_documento}/verificar", response_model=schemas.IntegridadDocumentoRespuesta)
def verificar_integridad(
    id_documento: str, archivo: UploadFile = File(...), db: Session = Depends(get_db)
):
    contenido_actual = leer_carga(archivo)
    return DocumentoService(db).verificar_integridad(id_documento, contenido_actual)
