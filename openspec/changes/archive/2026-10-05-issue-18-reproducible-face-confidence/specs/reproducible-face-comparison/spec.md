## ADDED Requirements

### Requirement: Comparación facial local reproducible

El sistema SHALL normalizar una comparación facial local a una confianza entre
0 y 1 y aplicar un umbral técnico documentado, sin presentarlo como precisión
biométrica ni identificación legal.

#### Scenario: Confidence meets the technical threshold

- **WHEN** la distancia LBPH se normaliza a 0.35
- **THEN** la comparación se considera coincidente

### Requirement: Captura facial atribuible y de calidad mínima

El sistema SHALL exigir una captura de por lo menos 120 × 120 píxeles, con
exactamente un rostro y nitidez mínima antes de comparar.

#### Scenario: Multiple faces are detected

- **WHEN** una captura contiene más de un rostro
- **THEN** la API devuelve 422 con `MULTIPLE_FACES_DETECTED`

#### Scenario: Quality is insufficient

- **WHEN** la captura no cumple resolución o nitidez mínima
- **THEN** la API devuelve 422 con `FACE_QUALITY_INSUFFICIENT`

### Requirement: Offline technical tests

La suite SHALL cubrir el umbral, errores negativos y veinte comparaciones con
fixtures sintéticas locales, sin cámara, red, modelo descargado ni biometría de
personas.

#### Scenario: Execute the face comparison suite offline

- **WHEN** pytest ejecuta las pruebas de comparación facial
- **THEN** completa los casos sin obtener recursos externos
