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

La matriz inicial de permisos asigna enrolamiento, edición, bloqueo,
credenciales y bitácora a `ADMINISTRADOR`; `OPERADOR` y `ADMINISTRADOR` pueden
iniciar y completar verificaciones. La API no confía en `id_responsable`
enviado por el cliente: lo toma del token. Un rol insuficiente retorna `403`
con `detail.code = AUTHORIZATION_REQUIRED`.

## Contrato de errores

Los errores de dominio usan `detail.code` estable y un mensaje seguro:
`CONSENT_REQUIRED` (409), `IDENTITY_NOT_FOUND` y `CREDENTIAL_NOT_FOUND` (404),
`SESSION_NOT_FOUND` (404), `SESSION_NOT_ACTIVE` (409), `FACE_NOT_DETECTED`
(422), `PROCEDURE_NOT_ENABLED` (409) y `DOCUMENT_NOT_FOUND` (404).

## Historial de sesiones

`GET /verificaciones` requiere `ADMINISTRADOR` y admite `resultado`,
`fecha_desde`, `fecha_hasta` e `id_identidad`. Devuelve responsable, factores,
decisión y fechas, sin imágenes ni rutas de biometría. Al consultar, cualquier
sesión `EN_CURSO` con más de diez minutos se materializa como `EXPIRADA` y no
acepta nuevos factores.

- /identidades y /identidades/consentimientos: datos ficticios y consentimiento.
- /credenciales: emisión, consulta, QR y revocación.
- /verificaciones: creación de sesión, rostro y prueba de vida.
- /documentos: hash y verificación de documentos de prueba.
- /auditoria: eventos y validación de cadena.
- /tramites: simulación condicionada a sesión aprobada.

Los routers y OpenAPI son la fuente de detalle de payloads. Al cambiar un endpoint, actualizar esta guía, pruebas de API y documentación OpenAPI.
