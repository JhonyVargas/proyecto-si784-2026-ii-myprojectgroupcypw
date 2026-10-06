# Compatibilidad, disponibilidad y observabilidad

## Why

RNF-03 y RNF-08 no tenían pruebas ni registro: no existía healthcheck, logs
operativos, monitoreo de disponibilidad ni evidencia en navegadores vigentes.

## What Changes

- Añadir `GET /salud` con estados ok, degradado y no_disponible, usado por
  Compose como healthcheck y por la estación como indicador.
- Registrar logs mínimos de acceso sin datos sensibles.
- Añadir `python -m benchmarks.monitor_disponibilidad` con criterio del 95 %.
- Añadir un recorrido automatizado en Chrome, Edge y Firefox con cámara
  simulada, cámara denegada y API caída, y documentar la matriz y resultados.
- Instalar en la imagen Docker las librerías EGL que MediaPipe requiere.
