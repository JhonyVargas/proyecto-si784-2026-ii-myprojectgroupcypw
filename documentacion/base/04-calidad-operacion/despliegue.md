# Ejecución y despliegue local

## Nativo

Desde backend: crear un entorno virtual, activarlo, instalar requirements.txt y ejecutar uvicorn app.main:app --reload.

En otra terminal, desde frontend: python -m http.server 5500. Visitar http://127.0.0.1:5500; API y Swagger: http://127.0.0.1:8000 y http://127.0.0.1:8000/docs.

Compose ofrece el equivalente local cuando Docker esté disponible. El volumen de datos es de desarrollo y puede reiniciarse; nunca contiene información real. Detener servicios con Ctrl+C o docker compose down.

## Configuración de persistencia

`NOTARYVERIFY_DATA_DIR` y `NOTARYVERIFY_DATABASE_URL` (solo SQLite) permiten
ubicar la base y los datos runtime; sin definirlas se usan `backend/data` y
`backend/data/notaryverify.db`, y en Compose el volumen `/app/data`. Si al
iniciar falta una columna en una tabla existente, el backend se detiene e indica
el reinicio: con el servidor detenido, desde backend, `python -m app.core.reset_db`
respalda la base en `<DATA_DIR>/respaldo/` y la recrea. En Compose:
`docker compose run --rm backend python -m app.core.reset_db`. Detalle en
[modelo de datos](../02-arquitectura/modelo-de-datos.md).
