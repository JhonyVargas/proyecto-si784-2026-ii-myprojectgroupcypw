# Trámite simulado en la interfaz del operador

## Why

El simulador SID-Sunarp y su evidencia existían en el backend, pero el operador
no podía enviar el trámite ni entender sus fallos desde la estación, y nada
distinguía el resultado del trámite del resultado de la verificación.

## What Changes

- Mostrar la sección de trámite solo con identidad verificada.
- Registrar un documento ficticio, elegir un escenario y enviar el trámite.
- Presentar el estado y la evidencia mínima aparte del veredicto, con reintento
  ante fallos externos y aviso de simulador académico.
- Probar por HTTP que un fallo externo no altera la sesión.
