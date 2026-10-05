"""Pruebas locales de la comparación facial reproducible (RF-05).

Usan arreglos sintéticos y adaptadores simulados: no descargan imágenes, no
requieren cámara y no afirman precisión biométrica.
"""

from time import perf_counter

import cv2
import numpy as np
import pytest

from app.services import biometria_service
from app.services.biometria_service import BiometriaService
from app.services.errors import (
    RostroCalidadInsuficienteError,
    RostroMultipleDetectadoError,
    RostroNoDetectadoError,
)


class _DetectorSimulado:
    def __init__(self, rostros):
        self.rostros = np.array(rostros)

    def detectMultiScale(self, *_args, **_kwargs):
        return self.rostros


class _ReconocedorSimulado:
    def __init__(self, distancia):
        self.distancia = distancia

    def train(self, *_args):
        pass

    def predict(self, *_args):
        return 0, self.distancia


@pytest.fixture()
def imagen_sintetica() -> bytes:
    """Patrón local con bordes; no representa ni contiene un rostro humano."""
    imagen = np.zeros((160, 160, 3), dtype=np.uint8)
    cv2.rectangle(imagen, (30, 30), (130, 130), (255, 255, 255), 3)
    cv2.line(imagen, (30, 30), (130, 130), (128, 128, 128), 2)
    _ok, codificada = cv2.imencode(".png", imagen)
    return codificada.tobytes()


def test_ausencia_de_rostro_es_normalizada_sin_red(monkeypatch, imagen_sintetica):
    monkeypatch.setattr(
        biometria_service, "_detector_rostros", lambda: _DetectorSimulado([])
    )
    with pytest.raises(RostroNoDetectadoError, match="No se detectó"):
        biometria_service._extraer_rostro(imagen_sintetica)


def test_multiples_rostros_son_rechazados_de_forma_determinista(monkeypatch, imagen_sintetica):
    monkeypatch.setattr(
        biometria_service,
        "_detector_rostros",
        lambda: _DetectorSimulado([[20, 20, 80, 80], [70, 70, 70, 70]]),
    )
    with pytest.raises(RostroMultipleDetectadoError, match="más de un rostro"):
        biometria_service._extraer_rostro(imagen_sintetica)


def test_calidad_minima_rechaza_imagen_de_baja_resolucion(monkeypatch):
    imagen = np.zeros((100, 100, 3), dtype=np.uint8)
    _ok, codificada = cv2.imencode(".png", imagen)
    monkeypatch.setattr(
        biometria_service, "_detector_rostros", lambda: pytest.fail("No debe invocar el detector")
    )
    with pytest.raises(RostroCalidadInsuficienteError, match="120 x 120"):
        biometria_service._extraer_rostro(codificada.tobytes())


def test_calidad_minima_rechaza_recorte_borroso(monkeypatch):
    imagen = np.zeros((160, 160, 3), dtype=np.uint8)
    _ok, codificada = cv2.imencode(".png", imagen)
    monkeypatch.setattr(
        biometria_service, "_detector_rostros", lambda: _DetectorSimulado([[20, 20, 100, 100]])
    )
    with pytest.raises(RostroCalidadInsuficienteError, match="demasiado borrosa"):
        biometria_service._extraer_rostro(codificada.tobytes())


@pytest.mark.parametrize(
    ("distancia", "esperado"), [(65.0, True), (65.01, False)]
)
def test_confianza_es_normalizada_y_aplica_umbral(monkeypatch, distancia, esperado):
    rostro = np.full((200, 200), 127, dtype=np.uint8)
    monkeypatch.setattr(biometria_service, "_extraer_rostro", lambda _imagen: rostro)
    monkeypatch.setattr(
        biometria_service.cv2.face,
        "LBPHFaceRecognizer_create",
        lambda: _ReconocedorSimulado(distancia),
    )
    coincide, confianza = BiometriaService().comparar_rostro(b"referencia", b"candidata")
    assert coincide is esperado
    assert 0.0 <= confianza <= 1.0
    assert confianza == round(1.0 - distancia / 100.0, 4)


def test_veinte_comparaciones_sinteticas_registran_latencia_local(monkeypatch):
    rostro = np.full((200, 200), 127, dtype=np.uint8)
    monkeypatch.setattr(biometria_service, "_extraer_rostro", lambda _imagen: rostro)
    monkeypatch.setattr(
        biometria_service.cv2.face,
        "LBPHFaceRecognizer_create",
        lambda: _ReconocedorSimulado(20.0),
    )
    latencias = []
    for _ in range(20):
        inicio = perf_counter()
        coincide, confianza = BiometriaService().comparar_rostro(b"r", b"c")
        latencias.append(perf_counter() - inicio)
        assert coincide is True
        assert confianza == 0.8
    assert len(latencias) == 20
    assert max(latencias) < 3.0
