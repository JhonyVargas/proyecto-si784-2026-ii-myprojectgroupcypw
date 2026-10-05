# Consulta segura mediante QR documental

## Why

La demostración documental necesitaba una consulta QR separada de las
credenciales, que comunicara integridad sin revelar el contenido ni datos de
la sesión.

## What Changes

- Publicar un contrato mínimo para el identificador opaco del QR documental.
- Recalcular el hash del archivo runtime al consultar.
- Limitar la respuesta a estado de integridad y fecha de generación.
