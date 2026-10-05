# Cambio: comparación facial reproducible

## Why

La prueba facial descargaba una imagen pública durante la ejecución y no
normalizaba calidad ni el caso de múltiples rostros. Eso impedía verificar
offline el umbral técnico de #18.

## What Changes

- Establecer preprocesamiento y calidad mínima explícitos.
- Normalizar los rechazos de ausencia, multiplicidad y baja calidad.
- Sustituir las pruebas de imagen externa por entradas sintéticas locales y
  veinte comparaciones repetibles.

## Fuera de alcance

No se mide precisión, FPR, liveness ni resistencia certificada ante ataques.
