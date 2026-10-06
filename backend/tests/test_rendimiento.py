"""Regresión controlada del benchmark técnico de RNF-02 y RNF-04 (#24).

Ejecuta el mismo benchmark con pocas repeticiones. Los detectores reales solo se
usan si ya existen localmente; en CI no se descargan y se mide el resto del
pipeline. No mide tiempo humano ni precisión biométrica.
"""

from benchmarks.medir_rendimiento import UMBRAL_COMPARACION_S, UMBRAL_FLUJO_S, ejecutar, resumen


def test_benchmark_cumple_umbrales_y_reporta_entorno():
    reporte = ejecutar(comparaciones=5, sesiones=3)

    assert reporte["comparacion_facial"]["n"] == 5
    assert reporte["comparacion_facial"]["promedio_s"] < UMBRAL_COMPARACION_S
    assert reporte["flujo_completo_sistema"]["n"] == 3
    assert reporte["flujo_completo_sistema"]["promedio_s"] < UMBRAL_FLUJO_S
    assert {"python", "opencv", "mediapipe", "detector_haar_real"} <= set(reporte["entorno"])


def test_resumen_calcula_metricas_y_cumplimiento():
    datos = resumen([1.0, 2.0, 3.0, 4.0], umbral=3.0)

    assert (datos["promedio_s"], datos["mediana_s"], datos["max_s"]) == (2.5, 2.5, 4.0)
    assert datos["cumple"] is True
    assert resumen([4.0], umbral=3.0)["cumple"] is False
