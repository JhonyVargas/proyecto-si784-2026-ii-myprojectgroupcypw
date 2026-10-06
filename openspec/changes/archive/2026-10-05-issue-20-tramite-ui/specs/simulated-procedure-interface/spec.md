## ADDED Requirements

### Requirement: Procedure action gated by verification

La estación SHALL ofrecer el trámite simulado únicamente cuando la sesión
termina con resultado IDENTIDAD_VERIFICADA.

#### Scenario: Verification is rejected

- **WHEN** la sesión termina con un resultado distinto de IDENTIDAD_VERIFICADA
- **THEN** la pantalla de resultado no muestra la acción de trámite

### Requirement: Procedure outcome separated from verification

La estación SHALL presentar el estado del trámite y su evidencia mínima aparte
del veredicto, y un fallo del servicio simulado SHALL NOT modificar el
resultado ni el estado de la sesión.

#### Scenario: External service fails and is retried

- **WHEN** el simulador responde SERVICIO_NO_DISPONIBLE y el operador reintenta con éxito
- **THEN** cada envío registra su propio trámite y la sesión conserva IDENTIDAD_VERIFICADA

### Requirement: Academic simulator notice

La sección de trámite SHALL indicar que se trata de un simulador académico sin
conexión con servicios institucionales reales y SHALL NOT mostrar rutas ni
detalles internos en sus mensajes de error.

#### Scenario: Procedure is not enabled

- **WHEN** el backend rechaza el trámite con PROCEDURE_NOT_ENABLED
- **THEN** la interfaz muestra un mensaje recuperable sin ruta ni huella del documento
