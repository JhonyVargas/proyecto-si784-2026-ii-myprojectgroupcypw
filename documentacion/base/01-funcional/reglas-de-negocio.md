# Reglas de negocio

- Una credencial válida solo recupera la identidad esperada; no aprueba la sesión.
- Credencial inexistente o revocada rechaza la verificación.
- Rostro no coincidente o prueba de vida fallida rechaza la verificación.
- La prueba de vida exige un desafío aleatorio emitido por el servidor, con 20
  segundos de vigencia y una única repetición; no guarda vídeo ni imágenes.
- La prueba de vida es experimental: una fotografía estática que no realiza la
  acción solicitada se rechaza en los escenarios controlados, sin afirmar que
  se reconozca todo soporte impreso o en pantalla.
- Credencial válida, rostro coincidente y vida superada permiten aprobar según las reglas configuradas.
- Tres o más intentos fallidos consecutivos generan alerta/bloqueo según la lógica existente.
- Toda sesión y evento crítico queda auditado; toda modificación documental se detecta por SHA-256.
- El uso de datos reales está prohibido.
