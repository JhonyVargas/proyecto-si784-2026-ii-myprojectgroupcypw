# Privacidad, CORS y cargas del entorno académico

## Why

La API aceptaba cualquier origen CORS, cargas de cualquier tipo y tamaño, y
creaba documentos sin credenciales, para sesiones inexistentes y con el
contenido en la URL, que queda en logs de acceso. El nombre del archivo del
documento derivaba de un dato del cliente.

## What Changes

- Orígenes CORS explícitos por entorno; `*` se rechaza al iniciar.
- Imágenes solo JPEG/PNG con firma coincidente y límite de tamaño configurable,
  validadas antes de los servicios.
- `POST /documentos` con rol, sesión existente y contenido en el cuerpo; archivo
  nombrado por el identificador interno.
- Guía de HTTPS para staging, secretos, logs mínimos y retención; pruebas de API
  y revisión estática de logs y secretos.
