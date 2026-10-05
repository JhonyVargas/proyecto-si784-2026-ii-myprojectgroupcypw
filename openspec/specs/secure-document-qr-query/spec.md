# secure-document-qr-query Specification

## Purpose

Permitir que una persona compruebe la integridad de un documento de prueba por
un identificador QR opaco, sin exponer el contenido ni información de identidad
o de la sesión de verificación.

## Requirements

### Requirement: Public minimum document QR query

El sistema SHALL resolver un identificador QR documental opaco mediante un
contrato distinto al de una credencial y SHALL devolver solamente el estado de
integridad y la fecha de generación.

#### Scenario: Intact document is queried

- **WHEN** se consulta el identificador QR de un documento runtime sin cambios
- **THEN** el contrato devuelve `INTEGRO` sin sesión, hash, contenido, identidad ni biometría

### Requirement: Runtime alteration is visible

El sistema SHALL recalcular el hash del contenido runtime antes de responder
una consulta QR documental.

#### Scenario: Stored document changes

- **WHEN** el contenido runtime ya no coincide con el hash registrado
- **THEN** el contrato devuelve `INTEGRIDAD_NO_VERIFICADA`
