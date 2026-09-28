# Proposal

## Why

La autenticación de #4 identifica al actor, pero aún no impedía que una cuenta
Operador accediera a operaciones administrativas o a la bitácora completa.

## What Changes

- Centralizar dependencias de rol y aplicar 401/403 a rutas API.
- Derivar el responsable de una verificación desde el token.
- Mostrar administración solo a Administrador en el cliente estático.

## Capabilities

### New Capabilities
- `role-authorization`: matriz de permisos local para Operador y Administrador.

### Modified Capabilities
- Ninguna.

## Impact

Rutas de identidad, credenciales, auditoría y verificación; interfaz y pruebas.
