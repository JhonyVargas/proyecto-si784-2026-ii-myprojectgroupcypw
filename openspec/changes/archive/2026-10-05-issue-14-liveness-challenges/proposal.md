# Cambio: desafío de prueba de vida experimental

## Why

La acción de vida se sorteaba en el navegador, no tenía vencimiento ni una
evidencia uniforme de repetición, y permitía una carga de archivo como
alternativa a cámara. La issue #14 requiere límites explícitos sin prometer una
defensa biométrica certificada.

## What Changes

- Emitir en servidor un desafío aleatorio, temporal y repetible una sola vez.
- Registrar emisión, vencimiento, resultado y motivo sin persistir vídeo.
- Normalizar ausencia/multiplicidad de rostro y eliminar la carga de archivo
  de la interfaz de vida.
- Probar negativos sintéticos de fotografía estática, impresa y en pantalla.

## Fuera de alcance

No se detecta el material físico de una imagen ni se evalúan ataques avanzados.
