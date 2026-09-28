# Proposal

## Why

No existe hardware RFID disponible, pero RF-03/RF-04 requieren una ruta de
credencial RFID verificable sin bloquear el QR ni fingir integración física.

## What Changes

- Registrar la decisión de no usar hardware físico durante esta etapa.
- Añadir un adaptador RFID simulado con UID hexadecimal canónico y el mismo contrato de lectura QR.

## Capabilities

### New Capabilities
- `simulated-rfid-credential`: lectura RFID local simulada sin hardware.

### Modified Capabilities
- Ninguna.

## Impact

Servicio/API de credenciales, pruebas, arquitectura y trazabilidad.
