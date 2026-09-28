# Reglas de negocio

- Una credencial válida solo recupera la identidad esperada; no aprueba la sesión.
- Credencial inexistente o revocada rechaza la verificación.
- Rostro no coincidente o prueba de vida fallida rechaza la verificación.
- Credencial válida, rostro coincidente y vida superada permiten aprobar según las reglas configuradas.
- Tres o más intentos fallidos consecutivos generan alerta/bloqueo según la lógica existente.
- Toda sesión y evento crítico queda auditado; toda modificación documental se detecta por SHA-256.
- El uso de datos reales está prohibido.
