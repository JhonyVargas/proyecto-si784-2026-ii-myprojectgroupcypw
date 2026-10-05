# recoverable-procedure-evidence Specification

## Purpose
Garantizar que un trámite académico simulado pueda reconstruirse desde la
sesión aprobada y el documento íntegro que lo habilitaron, sin revelar datos
sensibles ni integrarse con servicios institucionales reales.

## Requirements

### Requirement: Recoverable simulated procedure evidence

El sistema SHALL asociar cada trámite simulado con la sesión aprobada y el
documento de prueba que lo habilitaron mediante identificadores internos.

#### Scenario: Authorized evidence is reconstructed

- **WHEN** Administrador o Auditor consulta la evidencia de un trámite existente
- **THEN** obtiene identificadores, resultado de sesión, estado del trámite e
  integridad actual, sin contenido documental, hash, rutas, identidad ni biometría

### Requirement: Current document integrity is mandatory

El sistema SHALL volver a verificar la integridad vigente del documento antes
de crear un trámite simulado.

#### Scenario: Altered document blocks a procedure

- **WHEN** el contenido runtime del documento no coincide con su hash registrado
- **THEN** el trámite no se crea y se devuelve un error de integridad seguro

### Requirement: Critical evidence transitions are audited

El sistema SHALL registrar en la bitácora encadenada la asociación de evidencia
y la evaluación del trámite, sin incluir contenido documental ni biometría.

#### Scenario: Procedure is enabled

- **WHEN** una sesión aprobada y un documento íntegro habilitan un trámite
- **THEN** se registran los eventos de asociación y evaluación con identificadores internos
