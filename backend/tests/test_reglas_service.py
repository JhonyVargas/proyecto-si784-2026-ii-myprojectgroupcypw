"""Pruebas del motor de reglas de seguridad multicapa (RN-01)."""

import pytest

from app.models.enums import ResultadoVerificacion as R
from app.services.reglas_service import ReglasService


@pytest.mark.parametrize(
    "credencial_registrada,revocada,rostro,prueba_vida,esperado",
    [
        (False, False, None, None, R.CREDENCIAL_NO_REGISTRADA),
        (True, True, None, None, R.CREDENCIAL_REVOCADA),
        (True, False, False, None, R.ROSTRO_NO_COINCIDENTE),
        (True, False, True, False, R.PRUEBA_DE_VIDA_FALLIDA),
        (True, False, True, True, R.IDENTIDAD_VERIFICADA),
        (True, False, None, None, R.REQUIERE_REVISION),
    ],
)
def test_motor_de_reglas_cubre_todos_los_resultados_documentados(
    credencial_registrada, revocada, rostro, prueba_vida, esperado
):
    resultado = ReglasService().evaluar(credencial_registrada, revocada, rostro, prueba_vida)
    assert resultado == esperado


def test_credencial_revocada_prevalece_sobre_rostro_coincidente():
    """RN-01: ningún factor aislado aprueba una identidad."""

    resultado = ReglasService().evaluar(
        credencial_registrada=True,
        credencial_revocada=True,
        rostro_coincide=True,
        prueba_vida_superada=True,
    )
    assert resultado == R.CREDENCIAL_REVOCADA


def test_rostro_no_coincidente_prevalece_sobre_prueba_de_vida_superada():
    resultado = ReglasService().evaluar(
        credencial_registrada=True,
        credencial_revocada=False,
        rostro_coincide=False,
        prueba_vida_superada=True,
    )
    assert resultado == R.ROSTRO_NO_COINCIDENTE
