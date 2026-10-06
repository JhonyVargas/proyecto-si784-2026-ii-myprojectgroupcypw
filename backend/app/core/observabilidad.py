"""Salud y logs mínimos de operación (#25, RNF-03).

Los logs registran solo método, ruta sin query, estado y duración: nunca
cabeceras, tokens, cuerpos, imágenes ni documentos. Nivel configurable con
NOTARYVERIFY_LOG_LEVEL (por defecto INFO).
"""

from __future__ import annotations

import logging
import os
import sys
from time import perf_counter

from fastapi import Request
from sqlalchemy import text
from sqlalchemy.engine import Engine

logger = logging.getLogger("notaryverify.acceso")


def configurar_logs() -> None:
    raiz = logging.getLogger("notaryverify")
    if not raiz.handlers:
        manejador = logging.StreamHandler(sys.stderr)
        manejador.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
        raiz.addHandler(manejador)
    raiz.setLevel(os.getenv("NOTARYVERIFY_LOG_LEVEL") or "INFO")


async def registrar_acceso(request: Request, call_next):
    inicio = perf_counter()
    try:
        respuesta = await call_next(request)
    except Exception:
        logger.error("%s %s 500 %.1fms", request.method, request.url.path, (perf_counter() - inicio) * 1000)
        raise
    logger.info(
        "%s %s %s %.1fms",
        request.method, request.url.path, respuesta.status_code, (perf_counter() - inicio) * 1000,
    )
    return respuesta


def estado_salud(motor: Engine) -> tuple[int, dict]:
    """Comprueba la base y la presencia local de modelos, sin descargarlos."""
    from app.services.biometria_service import RUTA_CASCADA
    from app.services.liveness_service import RUTA_MODELO

    try:
        with motor.connect() as conexion:
            conexion.execute(text("SELECT 1"))
        base = "ok"
    except Exception:  # noqa: BLE001 (cualquier fallo de conexión es indisponibilidad)
        base = "error"

    modelos = {
        "haar_cascade": RUTA_CASCADA.exists() and RUTA_CASCADA.stat().st_size > 0,
        "mediapipe_face_landmarker": RUTA_MODELO.exists() and RUTA_MODELO.stat().st_size > 0,
    }
    if base != "ok":
        estado, codigo = "no_disponible", 503
    elif not all(modelos.values()):
        estado, codigo = "degradado", 200
    else:
        estado, codigo = "ok", 200
    return codigo, {"estado": estado, "base_datos": base, "modelos_locales": modelos}
