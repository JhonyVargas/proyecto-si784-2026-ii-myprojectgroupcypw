# Proposal

## Why

RN-09 exige que una referencia biométrica ficticia no pueda cambiarse por un
Operador de forma unilateral y que todo cambio sea trazable sin retener imágenes.

## What Changes

- Añadir solicitud con consentimiento vigente y decisión exclusiva de Administrador.
- Sustituir o eliminar referencias locales pendientes de forma segura y auditable.

## Capabilities

### New Capabilities
- `authorized-biometric-reference-change`: cambio local de referencia con aprobación trazable.

### Modified Capabilities
- Ninguna.

## Impact

Modelo SQLite aditivo, identidad, auditoría, API, pruebas y trazabilidad.
