# Design

`alertas_intentos_fallidos` es una tabla aditiva SQLite. Un rechazo durante la
vigencia retorna 423; el vencimiento resuelve la alerta al consultarla/operar y
un Administrador puede reactivarla con evidencia de auditoría. No se almacenan
muestras biométricas ni se cambia el estado permanente de identidad.
