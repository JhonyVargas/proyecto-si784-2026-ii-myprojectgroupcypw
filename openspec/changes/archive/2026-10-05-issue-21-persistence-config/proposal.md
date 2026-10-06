# Persistencia configurable y cambios de esquema verificados

## Why

La ruta SQLite estaba fijada en el código y `create_all` no detectaba una base
antigua incompatible: el error aparecía tarde, durante una operación, y no
existía un procedimiento reproducible para recuperarse.

## What Changes

- Leer `NOTARYVERIFY_DATA_DIR` y `NOTARYVERIFY_DATABASE_URL` con valores por
  defecto idénticos al prototipo y validar que la URL sea SQLite.
- Al iniciar, crear tablas aditivas y detener el arranque si faltan columnas.
- Añadir `python -m app.core.reset_db` para respaldar y recrear la base.
- Pasar la configuración por Docker Compose y documentar la decisión.

Compatibilidad: no se modifica ningún modelo; las bases existentes siguen
funcionando con los valores por defecto.
