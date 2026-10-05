# Evidencia recuperable de trámite simulado

## Why

Los artefactos de sesión, documento y trámite estaban persistidos por separado,
por lo que no era posible demostrar de manera recuperable cuál evidencia había
habilitado un trámite académico.

## What Changes

- Crear una asociación aditiva entre sesión aprobada, documento íntegro y
  trámite simulado.
- Verificar la integridad vigente y la pertenencia del documento antes del
  envío.
- Exponer una reconstrucción mínima únicamente a Administrador o Auditor y
  auditar las transiciones críticas.
