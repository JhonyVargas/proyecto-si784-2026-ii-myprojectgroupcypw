# Proposal

## Why

Las rutas del prototipo permiten actualmente operaciones sensibles sin una
identidad de operador verificable. La issue #4 es el cimiento de la ruta MVP:
sin autenticación local no es posible asignar responsable a una sesión ni
proteger las operaciones administrativas posteriores.

## What Changes

- Añadir usuarios locales de desarrollo con contraseñas derivadas mediante
  `scrypt`, nunca almacenadas en texto plano.
- Añadir inicio y cierre de sesión con tokens opacos, expiración configurable y
  revocación en persistencia local.
- Exponer dependencias FastAPI para obtener el usuario autenticado y respuestas
  401 estables para credenciales inválidas, revocadas o vencidas.
- Documentar la inicialización segura de usuarios de desarrollo y la
  compatibilidad de SQLite.

## Capabilities

### New Capabilities

- `local-authentication`: autenticación local y ciclo de vida de sesión para
  los roles académicos Operador y Administrador.

### Modified Capabilities

- Ninguna.

## Impact

Modelos SQLAlchemy, configuración de desarrollo, nuevas rutas `/auth`,
dependencias de API, pruebas y documentación de arquitectura/operación.
