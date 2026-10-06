"""Integridad documental mediante SHA-256 y QR de verificación (RF-09, RF-10, RN-08)."""

from __future__ import annotations

import hashlib
import io

import qrcode
from sqlalchemy.orm import Session

from app.core.database import DATA_DIR
from app.models import schemas
from app.models.db_models import DocumentoVerificado, SesionVerificacion
from app.services.errors import DocumentoNoEncontradoError, SesionNoEncontradaError

DOCUMENTOS_DIR = DATA_DIR / "documentos"
DOCUMENTOS_DIR.mkdir(parents=True, exist_ok=True)


class DocumentoService:
    def __init__(self, db: Session):
        self.db = db

    def generar_documento(self, id_sesion: str, contenido: str) -> DocumentoVerificado:
        if self.db.get(SesionVerificacion, id_sesion) is None:
            raise SesionNoEncontradaError(f"No existe la sesión '{id_sesion}'.")
        contenido_bytes = contenido.encode("utf-8")
        hash_sha256 = hashlib.sha256(contenido_bytes).hexdigest()

        documento = DocumentoVerificado(
            id_sesion=id_sesion,
            hash_sha256=hash_sha256,
            qr_verificacion="",
            contenido_path="",
        )
        self.db.add(documento)
        self.db.flush()
        # El archivo se nombra por el identificador interno del documento: el
        # cliente no controla la ruta (#22) y varios documentos de una misma
        # sesión no se sobrescriben entre sí.
        ruta = DOCUMENTOS_DIR / f"{documento.id}.txt"
        ruta.write_bytes(contenido_bytes)
        documento.contenido_path = str(ruta)
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

    @staticmethod
    def integridad_vigente(documento: DocumentoVerificado) -> bool:
        """Comprueba el archivo runtime sin exponer su contenido ni su hash."""
        try:
            contenido = open(documento.contenido_path, "rb").read()
        except OSError:
            return False
        return hashlib.sha256(contenido).hexdigest() == documento.hash_sha256

    def consultar_qr(self, identificador: str) -> schemas.ConsultaDocumentoRespuesta:
        """Consulta pública mínima: no filtra sesión, hash ni contenido."""
        documento = self.db.query(DocumentoVerificado).filter_by(qr_verificacion=identificador).first()
        if documento is None:
            raise DocumentoNoEncontradoError("No existe un documento para el identificador consultado.")
        integro = self.integridad_vigente(documento)
        return schemas.ConsultaDocumentoRespuesta(
            identificador=documento.qr_verificacion,
            estado="INTEGRO" if integro else "INTEGRIDAD_NO_VERIFICADA",
            fecha_generacion=documento.fecha_generacion,
        )
