# API

La API FastAPI se publica localmente en http://127.0.0.1:8000; Swagger está en /docs.

- /identidades y /identidades/consentimientos: datos ficticios y consentimiento.
- /credenciales: emisión, consulta, QR y revocación.
- /verificaciones: creación de sesión, rostro y prueba de vida.
- /documentos: hash y verificación de documentos de prueba.
- /auditoria: eventos y validación de cadena.
- /tramites: simulación condicionada a sesión aprobada.

Los routers y OpenAPI son la fuente de detalle de payloads. Al cambiar un endpoint, actualizar esta guía, pruebas de API y documentación OpenAPI.
