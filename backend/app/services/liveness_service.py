"""Prueba de vida experimental con MediaPipe Face Landmarker (RF-06).

Analiza una imagen asociada a un desafío aleatorio (parpadeo o giro de
rostro) y determina si la acción solicitada fue realizada, mediante puntos
y características faciales, según lo descrito en el FD01/FD02.

El modelo ``face_landmarker.task`` se descarga automáticamente (una sola
vez) desde el repositorio oficial de modelos de MediaPipe la primera vez
que se necesita, y se guarda en caché local en ``backend/data/modelos/``.
Si no hay conexión a internet disponible, se informa un error de dominio
claro en lugar de romper el arranque de toda la aplicación.

Nota de implementación: las coordenadas x de MediaPipe crecen hacia la
derecha de la imagen tal como la captura la cámara (sin espejar). El giro
"hacia la izquierda"/"hacia la derecha" se interpreta desde el punto de
vista de quien mira la imagen, no de la persona fotografiada.
"""

from __future__ import annotations

import urllib.error
import urllib.request

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

from app.core.database import DATA_DIR
from app.models.enums import AccionPruebaVida
from app.services.errors import RostroNoDetectadoError

MODELOS_DIR = DATA_DIR / "modelos"
MODELOS_DIR.mkdir(parents=True, exist_ok=True)
RUTA_MODELO = MODELOS_DIR / "face_landmarker.task"

URL_MODELO_OFICIAL = (
    "https://storage.googleapis.com/mediapipe-models/face_landmarker/"
    "face_landmarker/float16/1/face_landmarker.task"
)

# Índices de landmarks de la malla facial de MediaPipe Face Landmarker.
_OJO_IZQUIERDO = [33, 160, 158, 133, 153, 144]
_OJO_DERECHO = [362, 385, 387, 263, 373, 380]
_PUNTA_NARIZ = 1
_MEJILLA_IZQUIERDA = 234
_MEJILLA_DERECHA = 454

UMBRAL_EAR_CERRADO = 0.21
UMBRAL_GIRO = 0.15

_landmarker_cacheado: vision.FaceLandmarker | None = None


class ModeloNoDisponibleError(RuntimeError):
    """El modelo de MediaPipe no está disponible localmente ni se pudo descargar."""


def _asegurar_modelo_descargado() -> None:
    if RUTA_MODELO.exists() and RUTA_MODELO.stat().st_size > 0:
        return
    try:
        urllib.request.urlretrieve(URL_MODELO_OFICIAL, RUTA_MODELO)
    except (urllib.error.URLError, OSError) as exc:
        raise ModeloNoDisponibleError(
            "No fue posible descargar el modelo 'face_landmarker.task' de "
            "MediaPipe (se requiere conexión a internet la primera vez). "
            f"Puede descargarlo manualmente desde {URL_MODELO_OFICIAL} y "
            f"colocarlo en '{RUTA_MODELO}'."
        ) from exc


def _obtener_landmarker() -> vision.FaceLandmarker:
    global _landmarker_cacheado
    if _landmarker_cacheado is None:
        _asegurar_modelo_descargado()
        opciones = vision.FaceLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=str(RUTA_MODELO)),
            num_faces=1,
        )
        _landmarker_cacheado = vision.FaceLandmarker.create_from_options(opciones)
    return _landmarker_cacheado


def _distancia(p1, p2) -> float:
    return float(np.hypot(p1.x - p2.x, p1.y - p2.y))


def _ear(landmarks, indices) -> float:
    """Eye Aspect Ratio: disminuye marcadamente cuando el ojo está cerrado."""

    p = [landmarks[i] for i in indices]
    vertical_1 = _distancia(p[1], p[5])
    vertical_2 = _distancia(p[2], p[4])
    horizontal = _distancia(p[0], p[3])
    if horizontal == 0:
        return 1.0
    return (vertical_1 + vertical_2) / (2.0 * horizontal)


class LivenessService:
    def _landmarks(self, imagen_bytes: bytes):
        arreglo = np.frombuffer(imagen_bytes, dtype=np.uint8)
        imagen_bgr = cv2.imdecode(arreglo, cv2.IMREAD_COLOR)
        if imagen_bgr is None:
            raise RostroNoDetectadoError("El archivo recibido no es una imagen válida.")
        imagen_rgb = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)
        imagen_mp = mp.Image(image_format=mp.ImageFormat.SRGB, data=imagen_rgb)

        resultado = _obtener_landmarker().detect(imagen_mp)

        if not resultado.face_landmarks:
            raise RostroNoDetectadoError(
                "No se detectó ningún rostro para evaluar la prueba de vida."
            )
        return resultado.face_landmarks[0]

    def validar_accion(self, accion: str, imagen_bytes: bytes) -> tuple[bool, dict]:
        landmarks = self._landmarks(imagen_bytes)

        if accion == AccionPruebaVida.PARPADEO:
            ear = (_ear(landmarks, _OJO_IZQUIERDO) + _ear(landmarks, _OJO_DERECHO)) / 2.0
            superado = ear < UMBRAL_EAR_CERRADO
            return superado, {"metrica": "eye_aspect_ratio", "valor": round(ear, 4)}

        if accion not in (AccionPruebaVida.GIRO_IZQUIERDA, AccionPruebaVida.GIRO_DERECHA):
            raise ValueError(f"Acción de prueba de vida no soportada: '{accion}'.")

        nariz = landmarks[_PUNTA_NARIZ]
        mejilla_izq = landmarks[_MEJILLA_IZQUIERDA]
        mejilla_der = landmarks[_MEJILLA_DERECHA]
        ancho_rostro = abs(mejilla_der.x - mejilla_izq.x) or 1e-6
        centro = (mejilla_izq.x + mejilla_der.x) / 2.0
        desplazamiento = (nariz.x - centro) / ancho_rostro

        if accion == AccionPruebaVida.GIRO_IZQUIERDA:
            superado = desplazamiento > UMBRAL_GIRO
        else:
            superado = desplazamiento < -UMBRAL_GIRO

        return superado, {
            "metrica": "desplazamiento_horizontal",
            "valor": round(desplazamiento, 4),
        }
