# authorized-audit-recovery Specification

## Purpose
Permitir la recuperación verificable y autorizada de operaciones críticas de
una sesión, manteniendo el encadenamiento de hashes y minimizando los datos
expuestos por la interfaz de auditoría.

## Requirements

### Requirement: Authorized audit reconstruction

El sistema SHALL permitir únicamente a Administrador o Auditor reconstruir los
eventos críticos de una sesión existente.

#### Scenario: Auditor reconstructs a session

- **WHEN** un Auditor autorizado consulta una sesión
- **THEN** recibe tipo de evento, actor, entidad, identificador, payload mínimo,
  fecha y secuencia

### Requirement: Safe minimum audit payload

El sistema SHALL filtrar el detalle interno de cada evento mediante un catálogo
de campos públicos mínimos.

#### Scenario: Credential event is reconstructed

- **WHEN** se reconstruye un evento que contiene un código de credencial interno
- **THEN** el código no aparece en el payload público

### Requirement: Tamper detection remains available

El sistema SHALL conservar la verificación de la cadena hash y reportar el
primer evento alterado.

#### Scenario: Stored event is modified

- **WHEN** un evento persistido se modifica fuera del servicio de auditoría
- **THEN** la verificación reporta una cadena inválida y el primer evento alterado
