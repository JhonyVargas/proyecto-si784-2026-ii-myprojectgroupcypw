## ADDED Requirements

### Requirement: Explicit CORS origins

El backend SHALL permitir CORS solo a los orígenes de `NOTARYVERIFY_CORS_ORIGINS`
o, si no se definen, a la estación local, y SHALL negarse a iniciar con `*`.

#### Scenario: Unknown origin calls the API

- **WHEN** un origen no configurado envía una solicitud preflight
- **THEN** la respuesta no incluye `Access-Control-Allow-Origin`

### Requirement: Validated uploads without persistence

Las cargas de imágenes SHALL ser JPEG o PNG con firma coincidente y toda carga
SHALL respetar el límite configurado; una carga rechazada SHALL NOT crear filas
ni archivos.

#### Scenario: A GIF is uploaded as a reference

- **WHEN** un Administrador registra una identidad con una imagen GIF
- **THEN** la API responde 415 `UPLOAD_TYPE_NOT_ALLOWED` y no existe identidad ni archivo nuevo

### Requirement: Protected document creation

La creación de documentos SHALL exigir Operador o Administrador, una sesión
existente y el contenido en el cuerpo de la solicitud.

#### Scenario: Anonymous document creation

- **WHEN** se intenta crear un documento sin credenciales
- **THEN** la API responde 401 y no persiste el documento

### Requirement: Documented transport and secret handling

El repositorio SHALL documentar HTTPS para staging, manejo de secretos, logs
mínimos y retención de referencias, y SHALL verificar que no se versionen
secretos ni se registren datos sensibles.

#### Scenario: Static review runs in CI

- **WHEN** se ejecuta la suite de pruebas
- **THEN** falla si el código registra tokens, imágenes o documentos o si el repositorio contiene secretos
