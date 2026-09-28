# API

La API FastAPI se publica localmente en http://127.0.0.1:8000; Swagger está en /docs.

## Autenticación local de desarrollo

- `POST /auth/login` recibe `correo` y `password`, y devuelve `access_token`,
  vencimiento y el rol local. Se habilitan cuentas solo con las variables de
  bootstrap documentadas en `.env.example`; no hay credenciales por defecto.
- Las rutas que requieran una identidad autenticada usan
  `Authorization: Bearer <access_token>`. La ausencia, invalidez, revocación o
  vencimiento retorna `401` con `detail.code = AUTHENTICATION_REQUIRED`.
- `POST /auth/logout` revoca el token y `GET /auth/me` permite comprobar la
  sesión sin revelar una contraseña.

- /identidades y /identidades/consentimientos: datos ficticios y consentimiento.
- /credenciales: emisión, consulta, QR y revocación.
- /verificaciones: creación de sesión, rostro y prueba de vida.
- /documentos: hash y verificación de documentos de prueba.
- /auditoria: eventos y validación de cadena.
- /tramites: simulación condicionada a sesión aprobada.

Los routers y OpenAPI son la fuente de detalle de payloads. Al cambiar un endpoint, actualizar esta guía, pruebas de API y documentación OpenAPI.
