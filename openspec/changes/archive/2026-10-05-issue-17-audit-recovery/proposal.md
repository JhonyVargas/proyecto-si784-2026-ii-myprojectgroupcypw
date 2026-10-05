# Recuperación autorizada de bitácora encadenada

## Why

La cadena de hashes detectaba alteraciones, pero faltaba un contrato seguro que
permitiera recuperar una sesión crítica y catalogar sus operaciones sin exponer
los detalles internos de auditoría.

## What Changes

- Catalogar el payload público mínimo de eventos críticos.
- Permitir a Administrador o Auditor reconstruir una sesión existente.
- Probar acceso por rol, filtrado del detalle interno y detección de alteración.
