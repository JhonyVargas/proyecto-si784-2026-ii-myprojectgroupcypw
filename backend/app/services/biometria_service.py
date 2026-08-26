"""Reconocimiento facial local con OpenCV (RF-05, RF-06).

Utiliza únicamente herramientas de código abierto (Haar Cascade para
detección y LBPH — Local Binary Patterns Histograms — para comparación),
evitando depender de servicios comerciales o APIs biométricas de pago, tal
como se definió en el FD01/FD02 del proyecto.

Nota de entorno: las versiones recientes del paquete ``opencv-contrib-python``
(a partir de la serie 5.x) dejaron de incluir los archivos XML de Haar
Cascade dentro del propio paquete. Por ello, el clasificador se descarga
automáticamente (una sola vez) desde el repositorio oficial de OpenCV en
GitHub y se guarda en caché local en ``backend/data/modelos/``.
"""

from __future__ import annotations

import urllib.error
import urllib.request

import cv2
import numpy as np

from app.core.database import DATA_DIR
from app.services.errors import RostroNoDetectadoError

TAMANO_ROSTRO = (200, 200)
UMBRAL_COINCIDENCIA = 0.35
DISTANCIA_MAXIMA_NORMALIZACION = 100.0

MODELOS_DIR = DATA_DIR / "modelos"
MODELOS_DIR.mkdir(parents=True, exist_ok=True)
RUTA_CASCADA = MODELOS_DIR / "haarcascade_frontalface_default.xml"

URL_CASCADA_OFICIAL = (
    "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/"
    "haarcascade_frontalface_default.xml"
)

_detector_cacheado: cv2.CascadeClassifier | None = None


class ModeloNoDisponibleError(RuntimeError):
    """El clasificador Haar Cascade no está disponible localmente ni se pudo descargar."""


def _asegurar_cascada_descargada() -> None:
    if RUTA_CASCADA.exists() and RUTA_CASCADA.stat().st_size > 0:
        return
    try:
        urllib.request.urlretrieve(URL_CASCADA_OFICIAL, RUTA_CASCADA)
    except (urllib.error.URLError, OSError) as exc:
        raise ModeloNoDisponibleError(
            "No fue posible descargar el clasificador "
            "'haarcascade_frontalface_default.xml' de OpenCV (se requiere "
            "conexión a internet la primera vez). Puede descargarlo "
            f"manualmente desde {URL_CASCADA_OFICIAL} y colocarlo en "
            f"'{RUTA_CASCADA}'."
        ) from exc


def _detector_rostros() -> cv2.CascadeClassifier:
    global _detector_cacheado
    if _detector_cacheado is None:
        _asegurar_cascada_descargada()
        clasificador = cv2.CascadeClassifier(str(RUTA_CASCADA))
        if clasificador.empty():
            raise ModeloNoDisponibleError(
                f"El archivo de cascada en '{RUTA_CASCADA}' está corrupto o incompleto."
            )
        _detector_cacheado = clasificador
    return _detector_cacheado


def _decodificar(imagen_bytes: bytes) -> np.ndarray:
    arreglo = np.frombuffer(imagen_bytes, dtype=np.uint8)
    imagen = cv2.imdecode(arreglo, cv2.IMREAD_COLOR)
    if imagen is None:
        raise RostroNoDetectadoError("El archivo recibido no es una imagen válida.")
    return imagen


def _extraer_rostro(imagen_bytes: bytes) -> np.ndarray:
    imagen = _decodificar(imagen_bytes)
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    detector = _detector_rostros()
    rostros = detector.detectMultiScale(gris, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
    if len(rostros) == 0:
        raise RostroNoDetectadoError("No se detectó ningún rostro en la imagen proporcionada.")

    x, y, w, h = max(rostros, key=lambda r: r[2] * r[3])
    recorte = gris[y : y + h, x : x + w]
    recorte = cv2.resize(recorte, TAMANO_ROSTRO)
    return cv2.equalizeHist(recorte)


class BiometriaService:
    def comparar_rostro(
        self, imagen_referencia: bytes, imagen_candidata: bytes
    ) -> tuple[bool, float]:
        rostro_referencia = _extraer_rostro(imagen_referencia)
        rostro_candidato = _extraer_rostro(imagen_candidata)

        reconocedor = cv2.face.LBPHFaceRecognizer_create()
        reconocedor.train([rostro_referencia], np.array([0]))
        _etiqueta, distancia = reconocedor.predict(rostro_candidato)

        confianza = max(0.0, 1.0 - (distancia / DISTANCIA_MAXIMA_NORMALIZACION))
        coincide = confianza >= UMBRAL_COINCIDENCIA
        return coincide, round(confianza, 4)
