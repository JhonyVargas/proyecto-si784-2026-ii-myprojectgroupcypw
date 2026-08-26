"""Pruebas de integración de los módulos biométricos (RF-05, RF-06).

Usan una única imagen de referencia pública y ampliamente conocida
(``lena.jpg``, incluida históricamente en el propio repositorio de OpenCV
como imagen de prueba estándar). Si no hay conexión a internet disponible
en el entorno de ejecución, estas pruebas se omiten automáticamente en
lugar de fallar, ya que dependen de un recurso externo.
"""

import urllib.request

import pytest

from app.models.enums import AccionPruebaVida
from app.services.biometria_service import BiometriaService
from app.services.liveness_service import LivenessService

LENA_URL = "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/lena.jpg"


@pytest.fixture(scope="module")
def imagen_rostro_real() -> bytes:
    try:
        with urllib.request.urlopen(LENA_URL, timeout=5) as respuesta:
            return respuesta.read()
    except Exception:
        pytest.skip(
            "No hay conexión a internet disponible para descargar la imagen de "
            "prueba de referencia; se omite esta prueba de integración biométrica."
        )


def test_comparar_rostro_consigo_mismo_produce_alta_confianza(imagen_rostro_real):
    coincide, confianza = BiometriaService().comparar_rostro(
        imagen_rostro_real, imagen_rostro_real
    )
    assert coincide is True
    assert confianza > 0.9


def test_prueba_de_vida_parpadeo_no_superada_con_ojos_abiertos(imagen_rostro_real):
    superado, detalle = LivenessService().validar_accion(
        AccionPruebaVida.PARPADEO, imagen_rostro_real
    )
    assert superado is False
    assert detalle["metrica"] == "eye_aspect_ratio"
