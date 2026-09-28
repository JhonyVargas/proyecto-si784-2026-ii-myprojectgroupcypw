# Design

`LectorRfid` define un puerto para una futura integración física. El adaptador
actual solo acepta UID hexadecimal en mayúsculas y sin separadores; la tabla de
credenciales usa el UID como código RFID único. La lectura consulta la misma
credencial y estados de QR, y no participa en la decisión multicapa.
