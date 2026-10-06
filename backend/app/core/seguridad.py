"""Controles proporcionales de transporte y cargas del prototipo (#22).

- NOTARYVERIFY_CORS_ORIGINS: orígenes permitidos separados por comas
  (por defecto la estación local en el puerto 5500). "*" se rechaza.
- NOTARYVERIFY_MAX_UPLOAD_BYTES: tamaño máximo de una carga (por defecto 5 MB).

Ver documentacion/base/04-calidad-operacion/seguridad.md.
"""

from __future__ import annotations

import os
from collections.abc import Mapping

from fastapi import UploadFile

ORIGENES_POR_DEFECTO = ("http://127.0.0.1:5500", "http://localhost:5500")
MAX_UPLOAD_POR_DEFECTO = 5 * 1024 * 1024

# Firmas de los formatos de imagen aceptados; el Content-Type del cliente no basta.
_FIRMAS_IMAGEN = {
    "image/jpeg": (b"\xff\xd8\xff",),
    "image/png": (b"\x89PNG\r\n\x1a\n",),
}


class ConfiguracionSeguridadError(RuntimeError):
    """La configuración de seguridad del entorno no es válida."""


class CargaInvalidaError(Exception):
    """Carga rechazada antes de llegar a servicios o almacenamiento."""

    def __init__(self, status_code: int, code: str, message: str):
        super().__init__(message)
        self.status_code = status_code
        self.code = code


def resolver_origenes_cors(entorno: Mapping[str, str] = os.environ) -> list[str]:
    valor = entorno.get("NOTARYVERIFY_CORS_ORIGINS") or ",".join(ORIGENES_POR_DEFECTO)
    origenes = [o.strip().rstrip("/") for o in valor.split(",") if o.strip()]
    for origen in origenes:
        if origen == "*" or not origen.startswith(("http://", "https://")):
            raise ConfiguracionSeguridadError(
                f"Origen CORS no válido: '{origen}'. Use orígenes explícitos "
                "http(s)://host[:puerto]; '*' no está permitido."
            )
    return origenes


def resolver_max_upload(entorno: Mapping[str, str] = os.environ) -> int:
    valor = entorno.get("NOTARYVERIFY_MAX_UPLOAD_BYTES")
    if not valor:
        return MAX_UPLOAD_POR_DEFECTO
    if not valor.isdigit() or int(valor) <= 0:
        raise ConfiguracionSeguridadError("NOTARYVERIFY_MAX_UPLOAD_BYTES debe ser un entero positivo.")
    return int(valor)


MAX_UPLOAD_BYTES = resolver_max_upload()


def leer_carga(archivo: UploadFile, limite: int | None = None) -> bytes:
    """Lee la carga completa sin superar el límite; no la persiste."""
    limite = limite or MAX_UPLOAD_BYTES
    datos = archivo.file.read(limite + 1)
    if len(datos) > limite:
        raise CargaInvalidaError(
            413, "UPLOAD_TOO_LARGE", f"El archivo supera el máximo de {limite // 1024} KB."
        )
    if not datos:
        raise CargaInvalidaError(422, "UPLOAD_EMPTY", "El archivo está vacío.")
    return datos


def leer_imagen(archivo: UploadFile, limite: int | None = None) -> bytes:
    """Acepta solo JPEG o PNG cuyo contenido coincida con el tipo declarado."""
    tipo = (archivo.content_type or "").lower()
    if tipo not in _FIRMAS_IMAGEN:
        raise CargaInvalidaError(
            415, "UPLOAD_TYPE_NOT_ALLOWED", "Solo se aceptan imágenes JPEG o PNG."
        )
    datos = leer_carga(archivo, limite)
    if not datos.startswith(_FIRMAS_IMAGEN[tipo]):
        raise CargaInvalidaError(
            415, "UPLOAD_TYPE_NOT_ALLOWED", "El contenido no corresponde a una imagen JPEG o PNG."
        )
    return datos
