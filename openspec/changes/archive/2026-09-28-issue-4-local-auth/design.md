# Design

## Contexto

NotaryVerify es un prototipo local con SQLite. El modelo `Usuario` ya existe,
pero no había credenciales ni sesiones persistidas. La autenticación debe ser
segura y deliberadamente limitada al entorno de desarrollo académico.

## Decisiones

- Las contraseñas se derivan con `hashlib.scrypt` y una sal aleatoria; el valor
  almacenado incluye algoritmo, parámetros, sal y derivado codificados. No se
  añaden dependencias criptográficas ni contraseñas de ejemplo funcionales.
- El login entrega un token opaco aleatorio. Solo se persiste el SHA-256 del
  token, con fecha de expiración y revocación; el token nunca se registra en
  auditoría ni se guarda en el repositorio.
- `Authorization: Bearer <token>` es el contrato para las dependencias de API.
  Un token ausente, inválido, revocado o vencido devuelve `401` y el código
  estable `AUTHENTICATION_REQUIRED`, sin revelar qué dato falló.
- El bootstrap solo se habilita con variables de entorno explícitas. Por cada
  usuario se proporcionan correo, contraseña y rol; no hay cuenta por defecto.
  Las pruebas crean usuarios sintéticos directamente con el servicio.

## Persistencia y compatibilidad

Se incorpora únicamente la tabla aditiva `sesiones_usuario`. Las bases SQLite
locales existentes siguen siendo legibles; al iniciar, `create_all` crea la
nueva tabla sin modificar tablas existentes. No se pierde información. Si un
usuario requiere volver a probar el bootstrap, puede eliminar únicamente su
base local de desarrollo (`backend/data/notaryverify.db`) con el servidor
apagado; no es una migración productiva ni aplica a datos reales.

## Riesgos

Esto no ofrece SSO, recuperación de contraseña, límites de tasa ni despliegue
productivo. Esos controles quedan fuera de #4 y deberán evaluarse antes de
exponer el prototipo fuera de localhost.
