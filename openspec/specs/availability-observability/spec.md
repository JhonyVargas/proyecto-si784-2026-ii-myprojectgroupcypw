# availability-observability Specification

## Purpose
Dar señales operativas no identificables y evidencia de disponibilidad y de
compatibilidad con navegadores vigentes durante la evaluación académica.

## Requirements

### Requirement: Health endpoint

El backend SHALL exponer `GET /salud` que responda 200 `ok` con base y modelos
locales, 200 `degradado` si faltan modelos y 503 `no_disponible` si la base no
responde, sin exponer datos.

#### Scenario: Database is unreachable

- **WHEN** la base de datos no acepta conexiones
- **THEN** `/salud` responde 503 con estado `no_disponible`

### Requirement: Availability record with explicit criterion

El repositorio SHALL ofrecer un monitor que registre por sondeo fecha, código,
estado y latencia, y calcule la disponibilidad frente al 95 %.

#### Scenario: Availability falls below the threshold

- **WHEN** menos del 95 % de los sondeos responde 200
- **THEN** el resumen indica que no cumple y el comando termina con error

### Requirement: Minimal access logs

El backend SHALL registrar por solicitud solo método, ruta sin query, estado y
duración, y SHALL NOT registrar cabeceras, tokens, cuerpos, imágenes ni documentos.

#### Scenario: Login request is logged

- **WHEN** se envía un login con credenciales en el cuerpo y un token en la cabecera
- **THEN** el log contiene `POST /auth/login` y ningún dato de la solicitud

### Requirement: Understandable degradation in current browsers

La estación SHALL comunicar de forma comprensible la API caída y la cámara
denegada en Chrome, Edge y Firefox vigentes.

#### Scenario: Camera permission is denied

- **WHEN** el navegador rechaza la cámara con NotAllowedError
- **THEN** la estación explica cómo autorizarla y ofrece subir una fotografía
