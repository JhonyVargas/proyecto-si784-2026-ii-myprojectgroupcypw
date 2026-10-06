# configurable-persistence Specification

## Purpose
Hacer reproducible la configuración de la base SQLite y ofrecer un camino
seguro y verificable ante cambios de esquema del prototipo.

## Requirements

### Requirement: Environment-driven SQLite configuration

El backend SHALL obtener la carpeta de datos y la URL de la base desde
`NOTARYVERIFY_DATA_DIR` y `NOTARYVERIFY_DATABASE_URL`, usar las rutas del
prototipo cuando no estén definidas y rechazar URL que no sean SQLite.

#### Scenario: No variables are defined

- **WHEN** el backend inicia sin variables de persistencia
- **THEN** usa `backend/data/notaryverify.db`

#### Scenario: A server database URL is configured

- **WHEN** `NOTARYVERIFY_DATABASE_URL` no comienza con `sqlite://`
- **THEN** el arranque se detiene con un mensaje que indica que solo se admite SQLite

### Requirement: Verified schema on startup

Al iniciar, el backend SHALL crear las tablas nuevas y SHALL detener el
arranque si una tabla existente no tiene todas las columnas de los modelos.

#### Scenario: Existing table lacks a column

- **WHEN** una tabla existente no contiene una columna del modelo
- **THEN** el arranque falla listando `tabla.columna` y el comando de reinicio

### Requirement: Reproducible reset with backup

El repositorio SHALL ofrecer un comando que respalde la base SQLite de archivo y
la recree con el esquema vigente.

#### Scenario: Developer resets an incompatible database

- **WHEN** se ejecuta `python -m app.core.reset_db`
- **THEN** la base anterior queda en `<DATA_DIR>/respaldo/` y la nueva tiene el esquema vigente
