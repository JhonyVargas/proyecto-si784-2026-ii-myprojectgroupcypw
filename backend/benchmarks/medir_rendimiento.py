"""Benchmark técnico reproducible de RNF-02 y RNF-04 (#24).

Uso, desde backend:

    python -m benchmarks.medir_rendimiento --comparaciones 20 --sesiones 20 --salida reporte.json

Mide el costo de cómputo del sistema con imágenes sintéticas (ruido con
semilla fija, sin rostros de personas). Los detectores reales (Haar Cascade y
MediaPipe Face Landmarker) se ejecutan si ya existen en la carpeta de modelos
local; nunca se descargan. Como las imágenes no contienen rostros, la posición
del rostro y el resultado de la acción de vida se inyectan después de ejecutar
el detector real: se mide su costo, no su precisión. El tiempo humano frente a
la cámara no forma parte de esta medición (ver estrategia de pruebas).
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import statistics
import sys
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

import cv2
import numpy as np

UMBRAL_COMPARACION_S = 3.0   # RNF-02: comparación facial promedio
UMBRAL_FLUJO_S = 45.0        # RNF-04: flujo completo
ANCHO, ALTO = 640, 480
ROSTRO_INYECTADO = np.array([[220, 140, 200, 200]])


def imagen_sintetica(semilla: int) -> bytes:
    """JPEG 640x480 de ruido suavizado: textura con nitidez suficiente y sin rostros."""
    generador = np.random.default_rng(semilla)
    ruido = generador.integers(0, 256, (ALTO, ANCHO, 3), dtype=np.uint8)
    imagen = cv2.GaussianBlur(ruido, (3, 3), 0)
    _ok, codificada = cv2.imencode(".jpg", imagen, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return codificada.tobytes()


def entorno(detector_real: bool, landmarker_real: bool) -> dict:
    import fastapi
    import mediapipe

    return {
        "fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sistema": f"{platform.system()} {platform.release()}",
        "procesador": platform.processor() or platform.machine(),
        "nucleos_logicos": os.cpu_count(),
        "python": platform.python_version(),
        "opencv": cv2.__version__,
        "mediapipe": mediapipe.__version__,
        "fastapi": fastapi.__version__,
        "detector_haar_real": detector_real,
        "mediapipe_landmarker_real": landmarker_real,
        "imagen": f"JPEG sintético {ANCHO}x{ALTO}",
    }


def resumen(tiempos: list[float], umbral: float) -> dict:
    ordenados = sorted(tiempos)
    p95 = ordenados[max(0, round(0.95 * len(ordenados)) - 1)]
    promedio = statistics.fmean(tiempos)
    return {
        "n": len(tiempos),
        "promedio_s": round(promedio, 4),
        "mediana_s": round(statistics.median(tiempos), 4),
        "p95_s": round(p95, 4),
        "min_s": round(ordenados[0], 4),
        "max_s": round(ordenados[-1], 4),
        "umbral_s": umbral,
        "cumple": promedio < umbral,
    }


@contextmanager
def adaptadores_medibles():
    """Ejecuta los detectores reales disponibles e inyecta rostro y acción."""
    import app.services.biometria_service as biometria
    import app.services.liveness_service as liveness

    detector_real = biometria.RUTA_CASCADA.exists() and biometria.RUTA_CASCADA.stat().st_size > 0
    landmarker_real = liveness.RUTA_MODELO.exists() and liveness.RUTA_MODELO.stat().st_size > 0
    cascada = cv2.CascadeClassifier(str(biometria.RUTA_CASCADA)) if detector_real else None

    class DetectorMedido:
        def detectMultiScale(self, gris, **parametros):  # noqa: N802 (API de OpenCV)
            if cascada is not None:
                cascada.detectMultiScale(gris, **parametros)
            return ROSTRO_INYECTADO

    validar_original = liveness.LivenessService.validar_accion

    def validar_medido(servicio, accion, imagen_bytes):
        if landmarker_real:
            try:
                servicio._landmarks(imagen_bytes)
            except liveness.RostroNoDetectadoError:
                pass
        return True, {"metrica": "benchmark", "experimental": True}

    detector_original = biometria._detector_rostros
    biometria._detector_rostros = DetectorMedido
    liveness.LivenessService.validar_accion = validar_medido
    try:
        yield detector_real, landmarker_real
    finally:
        biometria._detector_rostros = detector_original
        liveness.LivenessService.validar_accion = validar_original


def medir_comparaciones(n: int) -> list[float]:
    from app.services.biometria_service import BiometriaService

    servicio = BiometriaService()
    referencia = imagen_sintetica(0)
    tiempos = []
    for i in range(n):
        candidata = imagen_sintetica(i + 1)
        inicio = perf_counter()
        servicio.comparar_rostro(referencia, candidata)
        tiempos.append(perf_counter() - inicio)
    return tiempos


def medir_sesiones(n: int) -> list[float]:
    """n sesiones HTTP completas: inicio, rostro, desafío y prueba de vida."""
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool

    import app.services.identidad_service as identidad
    from app.core.database import Base, get_db
    from app.main import app
    from app.models import db_models  # noqa: F401
    from app.models import schemas
    from app.models.enums import RolUsuario
    from app.services.auth_service import AuthService
    from app.services.consentimiento_service import ConsentimientoService
    from app.services.credencial_service import CredencialService
    from app.services.identidad_service import IdentidadService

    motor = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(bind=motor)
    db = sessionmaker(bind=motor, autoflush=False, autocommit=False)()
    referencias_original = identidad.REFERENCIAS_DIR
    tiempos = []
    with tempfile.TemporaryDirectory() as carpeta:
        identidad.REFERENCIAS_DIR = Path(carpeta)
        app.dependency_overrides[get_db] = lambda: db
        try:
            ConsentimientoService(db).otorgar(schemas.ConsentimientoCrear(id_participante="benchmark"))
            persona = IdentidadService(db).registrar(schemas.IdentidadCrear(
                nombre_ficticio="PERSONA-BENCHMARK", documento_ficticio="BENCH-001",
                id_participante="benchmark", confirmo_dato_ficticio=True,
            ), imagen_sintetica(0))
            codigo = CredencialService(db).emitir(schemas.CredencialCrear(id_identidad=persona.id)).codigo
            AuthService(db).create_user("Operador", "operador.bench@example.test", "clave-bench", RolUsuario.OPERADOR)

            cliente = TestClient(app)  # sin lifespan: no toca la base runtime
            for i in range(n):
                captura = imagen_sintetica(100 + i)
                inicio = perf_counter()
                token = cliente.post("/auth/login", json={
                    "correo": "operador.bench@example.test", "password": "clave-bench",
                }).json()["access_token"]
                h = {"Authorization": f"Bearer {token}"}
                sesion = cliente.post("/verificaciones", headers=h, json={"codigo_credencial": codigo}).json()
                cliente.post(f"/verificaciones/{sesion['id']}/rostro", headers=h,
                             files={"imagen": ("r.jpg", captura, "image/jpeg")}).raise_for_status()
                cliente.post(f"/verificaciones/{sesion['id']}/prueba-vida/desafio", headers=h).raise_for_status()
                final = cliente.post(f"/verificaciones/{sesion['id']}/prueba-vida", headers=h,
                                     files={"imagen": ("v.jpg", captura, "image/jpeg")})
                tiempos.append(perf_counter() - inicio)
                final.raise_for_status()
                if final.json()["resultado"] != "IDENTIDAD_VERIFICADA":
                    raise RuntimeError(f"La sesión {i} no terminó aprobada: {final.json()['resultado']}")
        finally:
            app.dependency_overrides.clear()
            identidad.REFERENCIAS_DIR = referencias_original
            db.close()
            motor.dispose()
    return tiempos


def ejecutar(comparaciones: int, sesiones: int) -> dict:
    with adaptadores_medibles() as (detector_real, landmarker_real):
        medir_comparaciones(1)  # calentamiento: carga perezosa de modelos
        reporte = {
            "entorno": entorno(detector_real, landmarker_real),
            "comparacion_facial": resumen(medir_comparaciones(comparaciones), UMBRAL_COMPARACION_S),
            "flujo_completo_sistema": resumen(medir_sesiones(sesiones), UMBRAL_FLUJO_S),
        }
    return reporte


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--comparaciones", type=int, default=20)
    parser.add_argument("--sesiones", type=int, default=20)
    parser.add_argument("--salida", type=Path)
    args = parser.parse_args()

    reporte = ejecutar(args.comparaciones, args.sesiones)
    texto = json.dumps(reporte, ensure_ascii=False, indent=2)
    if args.salida:
        args.salida.write_text(texto + "\n", encoding="utf-8")
    print(texto)
    cumple = reporte["comparacion_facial"]["cumple"] and reporte["flujo_completo_sistema"]["cumple"]
    return 0 if cumple else 1


if __name__ == "__main__":
    sys.exit(main())
