# Diseño: desafío de prueba de vida

Una tabla aditiva `desafios_prueba_vida` conserva únicamente acción, estado,
emisión, vencimiento y repetición. La captura sigue siendo efímera. El backend
elige entre parpadeo y giros, acepta una sola sustitución y termina la sesión
como fallida si vence. La acción enviada por el cliente no participa en la
decisión.

MediaPipe analiza hasta dos rostros para rechazar entradas ambiguas. Las pruebas
usan landmarks y capturas sintéticas; una imagen estática que no cumple el giro
representa los ataques de fotografía impresa y en pantalla soportados.
