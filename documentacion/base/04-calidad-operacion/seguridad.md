# Seguridad y privacidad

- Usar exclusivamente identidades, documentos y números ficticios.
- Registrar biometría solo de voluntarios con consentimiento explícito y propósito académico.
- No versionar fotos, cargas, modelos descargados, SQLite runtime, tokens ni credenciales.
- Los QR contienen identificadores o tokens, no información biométrica ni personal.
- Auditoría encadenada y SHA-256 son evidencia experimental, no certificación legal.
- Reportar exposición o pérdida de datos de prueba al equipo y detener su uso hasta evaluar el incidente.

## Controles del prototipo (#22)

Son controles proporcionales a un prototipo académico local o de staging; no
constituyen una certificación de seguridad ni habilitan datos reales.

### Orígenes CORS

`NOTARYVERIFY_CORS_ORIGINS` lista, separados por comas, los orígenes exactos que
pueden llamar a la API (por defecto `http://127.0.0.1:5500` y
`http://localhost:5500`). El backend no inicia si la lista contiene `*` o un
valor sin esquema `http(s)://`. Solo se permiten los métodos GET, POST, PATCH y
OPTIONS y las cabeceras `Authorization` y `Content-Type`. En staging se define
únicamente el origen HTTPS del frontend, por ejemplo
`NOTARYVERIFY_CORS_ORIGINS=https://notaryverify-staging.example.test`.

### Cargas

Las imágenes biométricas (registro, cambio de referencia, rostro y prueba de
vida) se aceptan solo como JPEG o PNG y su contenido debe coincidir con la firma
del formato declarado. Toda carga, incluido el archivo de verificación de
integridad, se limita a `NOTARYVERIFY_MAX_UPLOAD_BYTES` (por defecto 5 MB). La
validación ocurre antes de invocar servicios: una carga rechazada no crea filas
ni archivos y responde `UPLOAD_TYPE_NOT_ALLOWED` (415), `UPLOAD_TOO_LARGE` (413)
o `UPLOAD_EMPTY` (422).

La creación de documentos exige Operador o Administrador, una sesión existente y
el contenido en el cuerpo del formulario (máximo 20 000 caracteres); el archivo
se nombra con el identificador interno del documento, no con datos del cliente.

### HTTPS/TLS en staging (RNF-07)

El backend y el servidor estático no terminan TLS. Para un staging académico:

1. Publicar backend y frontend detrás de un proxy inverso con certificado
   válido (por ejemplo Caddy con certificados automáticos, o nginx con Let's
   Encrypt), redirigiendo HTTP a HTTPS y enviando
   `Strict-Transport-Security`.
2. Exponer al exterior solo el puerto 443 del proxy; uvicorn escucha en una red
   interna o en `127.0.0.1`.
3. Definir `window.NOTARYVERIFY_API = "https://api-staging.example.test"` en un
   `<script>` previo a `app.js` y el mismo origen del frontend en
   `NOTARYVERIFY_CORS_ORIGINS`. Los navegadores solo conceden la cámara en
   HTTPS o en `localhost`.
4. No reutilizar en staging cuentas, bases ni volúmenes de desarrollo.

### Secretos

Las contraseñas de las cuentas de arranque (`NOTARYVERIFY_BOOTSTRAP_*`) y
cualquier otro secreto se definen como variables de entorno o en un `.env` local
que Git ignora; `.env.example` solo contiene marcadores. Los tokens de sesión se
guardan como hash SHA-256 y el frontend los conserva en `sessionStorage`, que se
borra al cerrar la pestaña. `test_security_hardening.py` revisa que el
repositorio no versione claves privadas, tokens ni asignaciones de contraseñas.

### Logs mínimos

El backend no escribe imágenes, tokens, contraseñas, hashes ni contenido de
documentos en logs; una prueba estática rechaza `print`/`logging` con esos
datos. El log de acceso de uvicorn registra método, ruta e identificadores
internos; el contenido de documentos ya no viaja en la URL. En staging puede
desactivarse con `uvicorn ... --no-access-log` si no se requiere.

### Retención de referencias

Las referencias faciales activas viven en `<DATA_DIR>/referencias_faciales` y
las pendientes en `<DATA_DIR>/referencias_pendientes`; una solicitud decidida
elimina su archivo pendiente. Al terminar cada periodo de evaluación, o si un
voluntario retira su consentimiento, el equipo elimina su referencia y, para un
reinicio completo, la carpeta de datos (`docker compose down -v` en Compose).
`python -m app.core.reset_db` reinicia la base pero no borra las referencias.
