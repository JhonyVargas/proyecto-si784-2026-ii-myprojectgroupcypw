# configurable-multilayer-rules Specification

## Purpose

Permitir prioridades multicapa administrables y reproducibles sin relajar los
factores de seguridad obligatorios.

## Requirements

### Requirement: Versioned mandatory rule priorities

El sistema SHALL permitir que Administrador o Auditor versionen únicamente el
orden de CREDENCIAL, ROSTRO y PRUEBA_VIDA; SHALL NOT permitir desactivar factores.

#### Scenario: Invalid catalog is rejected

- **WHEN** una configuración omite o repite un factor obligatorio
- **THEN** no entra en vigencia

### Requirement: Reproducible rule decision

El sistema SHALL asociar cada resultado de sesión con la versión e instantánea
de la configuración aplicada.

#### Scenario: Decision is inspected

- **WHEN** se consulta la evidencia de una decisión
- **THEN** se puede identificar la configuración de reglas aplicada
