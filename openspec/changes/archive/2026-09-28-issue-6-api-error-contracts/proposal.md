# Proposal

## Why

Los errores del dominio se traducían de forma desigual en cada router, haciendo
que UI y pruebas dependieran de textos internos.

## What Changes

- Unificar los rechazos de dominio en estado HTTP y `detail.code` estable.

## Capabilities

### New Capabilities
- `api-error-contracts`: respuestas de error HTTP estables para el dominio.

### Modified Capabilities
- Ninguna.

## Impact

Aplicación FastAPI, routers, documentación y pruebas API.
