## ADDED Requirements

### Requirement: Server-issued experimental liveness challenge

El sistema SHALL emitir la acción de prueba de vida en el servidor, con una
vigencia de 20 segundos y a lo sumo una repetición, antes de aceptar una
captura.

#### Scenario: Challenge expires

- **WHEN** una captura llega después del vencimiento
- **THEN** la sesión finaliza como `PRUEBA_DE_VIDA_FALLIDA` y deja evidencia de timeout

### Requirement: Minimal traceability without biometric media

El sistema SHALL registrar acción, emisión, vencimiento, repetición, resultado y motivo, pero SHALL NOT persistir vídeo, imagen ni landmarks de vida.

#### Scenario: Controlled static attack

- **WHEN** una captura estática no cumple el desafío emitido
- **THEN** la prueba de vida se rechaza con un motivo trazable

### Requirement: Experimental limits visible to the operator

La interfaz SHALL requerir cámara en vivo y explicar que la prueba es
experimental, sin afirmar detección certificada de papel o pantalla.

#### Scenario: Camera access is denied

- **WHEN** el navegador deniega la cámara
- **THEN** la interfaz explica que debe recuperar el permiso o reiniciar la verificación
