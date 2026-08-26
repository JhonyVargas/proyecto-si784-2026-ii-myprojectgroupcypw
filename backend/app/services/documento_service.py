"""Integridad documental mediante SHA-256 y QR de verificación (RF-09, RF-10, RN-08)."""

from __future__ import annotations

import hashlib
import io

import qrcode
from sqlalchemy.orm import Session

from app.core.database import DATA_DIR
from app.models import schemas
from app.models.db_models import DocumentoVerificado
from app.services.errors import DocumentoNoEncontradoError

DOCUMENTOS_DIR = DATA_DIR / "documentos"
DOCUMENTOS_DIR.mkdir(parents=True, exist_ok=True)


class DocumentoService:
    def __init__(self, db: Session):
        self.db = db

    def generar_documento(self, id_sesion: str, contenido: str) -> DocumentoVerificado:
        contenido_bytes = contenido.encode("utf-8")
        hash_sha256 = hashlib.sha256(contenido_bytes).hexdigest()

        ruta = DOCUMENTOS_DIR / f"{id_sesion}.txt"
        ruta.write_bytes(contenido_bytes)

        documento = DocumentoVerificado(
            id_sesion=id_sesion,
            hash_sha256=hash_sha256,
            qr_verificacion="",
            contenido_path=str(ruta),
        )
        self.db.add(documento)
        self.db.flush()
        # El QR solo codifica un identificador de consulta; nunca datos
        # personales (ver FD02, sección "Otros requerimientos del producto").
        documento.qr_verificacion = f"NOTARYVERIFY-DOC-{documento.id}"
        self.db.commit()
        self.db.refresh(documento)
        return documento

    def generar_imagen_qr(self, documento: DocumentoVerificado) -> bytes:
        imagen = qrcode.make(documento.qr_verificacion)
        buffer = io.BytesIO()
        imagen.save(buffer, format="PNG")
        return buffer.getvalue()

    def verificar_integridad(
        self, id_documento: str, contenido_actual: bytes
    ) -> schemas.IntegridadDocumentoRespuesta:
        documento = self.db.get(DocumentoVerificado, id_documento)
        if documento is None:
            raise DocumentoNoEncontradoError(f"No existe el documento '{id_documento}'.")
        hash_calculado = hashlib.sha256(contenido_actual).hexdigest()
        return schemas.IntegridadDocumentoRespuesta(
            integro=hash_calculado == documento.hash_sha256,
            hash_esperado=documento.hash_sha256,
            hash_calculado=hash_calculado,
        )
