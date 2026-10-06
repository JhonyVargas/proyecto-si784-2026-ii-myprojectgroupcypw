## ADDED Requirements

### Requirement: Reproducible technical benchmark

El repositorio SHALL ofrecer un benchmark que mida la comparación facial y el
flujo HTTP completo con imágenes sintéticas, sin descargar modelos ni usar
rostros de personas, y que reporte el entorno y promedio, mediana, p95, mínimo y
máximo frente a los umbrales de RNF-02 y RNF-04.

#### Scenario: Benchmark is executed

- **WHEN** se ejecuta `python -m benchmarks.medir_rendimiento`
- **THEN** el reporte incluye entorno, métricas y cumplimiento, y el comando falla si un promedio supera su umbral

### Requirement: Controlled performance regression

La suite de pruebas SHALL ejecutar una versión reducida del benchmark y fallar
si algún promedio supera su umbral.

#### Scenario: A change slows the pipeline beyond the threshold

- **WHEN** el promedio de comparación supera 3 s o el del flujo supera 45 s
- **THEN** `test_rendimiento` falla en pytest y en CI

### Requirement: Declared measurement limits

Los resultados SHALL declarar qué se inyecta, que no incluyen tiempo humano ni
precisión biométrica y qué decisión se tomó ante desviaciones.

#### Scenario: Reading the performance report

- **WHEN** se consulta `rendimiento.md`
- **THEN** distingue el benchmark técnico de la medición con cámara y registra las decisiones sobre desviaciones
