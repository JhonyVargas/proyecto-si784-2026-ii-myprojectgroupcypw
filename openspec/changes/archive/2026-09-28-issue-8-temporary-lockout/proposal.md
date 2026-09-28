# Proposal

## Why

RN-05 exige alerta y bloqueo temporal tras tres rechazos, no la desactivación
permanente que mantenía la implementación inicial.

## What Changes

- Registrar alertas auditables, bloquear por 15 minutos y permitir vencimiento o reactivación administrativa.

## Capabilities

### New Capabilities
- `temporary-verification-lockout`: alerta y recuperación controlada RN-05.

### Modified Capabilities
- Ninguna.

## Impact

Persistencia aditiva, verificación, API, auditoría, pruebas y documentación.
