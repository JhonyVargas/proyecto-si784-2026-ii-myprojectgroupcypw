# Benchmark reproducible de rendimiento

## Why

RNF-02 y RNF-04 no tenían protocolo ni reporte; solo existía una guarda con
adaptadores simulados que no ejecutaba los detectores reales.

## What Changes

- Añadir `python -m benchmarks.medir_rendimiento`, que mide 20 comparaciones y
  20 sesiones HTTP con imágenes sintéticas y detectores reales locales.
- Registrar entorno, promedio, mediana, p95, mínimo, máximo y cumplimiento.
- Añadir una regresión controlada en pytest y CI.
- Documentar protocolo, resultados, limitaciones, medición con cámara pendiente
  y la decisión sobre desviaciones.
