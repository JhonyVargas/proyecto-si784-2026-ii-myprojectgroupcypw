# Compatibilidad, disponibilidad y observabilidad (#25)

Evidencia de RNF-08 (navegadores vigentes) y RNF-03 (disponibilidad del 95 %
durante el periodo de evaluación), con señales operativas no identificables.

## Matriz de navegadores

`frontend/e2e/recorrido_navegadores.py` ejecuta tres escenarios por navegador
con la cámara simulada que provee el propio navegador (sin personas ni
imágenes reales):

| Escenario | Qué comprueba |
| --- | --- |
| `flujo_camara` | API conectada, login de Operador, credencial válida, vídeo en vivo y captura; el fotograma sintético no tiene rostro y la estación muestra el motivo sin perder la sesión |
| `camara_denegada` | `getUserMedia` rechaza con `NotAllowedError`; la estación explica cómo autorizar la cámara y ofrece subir una fotografía |
| `api_caida` | las llamadas a la API fallan; el indicador muestra "API no disponible" y el login explica la causa |

Ejecución (backend y frontend locales en marcha):

```
pip install -r frontend/e2e/requirements.txt
python -m playwright install firefox
python frontend/e2e/recorrido_navegadores.py --salida resultados.json
```

Las cuentas se toman de `NOTARYVERIFY_E2E_ADMIN_EMAIL/PASSWORD` y
`NOTARYVERIFY_E2E_OPERATOR_EMAIL/PASSWORD`; el script crea una identidad y una
credencial ficticias con una imagen gris sintética.

### Resultados del 2026-10-05 (Windows 11)

| Navegador | Versión | flujo_camara | camara_denegada | api_caida |
| --- | --- | --- | --- | --- |
| Google Chrome | 154.0.8037.98 | Aprobado | Aprobado | Aprobado |
| Microsoft Edge | 154.0.4258.53 | Aprobado | Aprobado | Aprobado |
| Firefox (build de Playwright) | 155.0 | Aprobado | Aprobado | Aprobado |

Mensajes observados: "No se detectó ningún rostro en la imagen proporcionada.";
"Se denegó el permiso de cámara. Autorícelo desde el icono de la barra de
direcciones y recargue la página."; "No se pudo contactar con la API. Verifique
que el backend esté en ejecución."

Limitaciones: la cámara es simulada, por lo que el recorrido no llega a una
aprobación biométrica; Firefox es la compilación de Playwright, no la instalada;
no se probó macOS ni móviles. El recorrido aprobado con rostro real queda en la
[lista manual](estrategia-pruebas.md#recorrido-manual-mvp-por-navegador) y en
la demostración final (#29).

## Healthcheck

`GET /salud` es público y no expone datos:

| Estado | HTTP | Criterio |
| --- | --- | --- |
| `ok` | 200 | la base responde a `SELECT 1` y los modelos Haar y MediaPipe existen localmente |
| `degradado` | 200 | la base responde pero falta algún modelo; se descargará en la primera captura |
| `no_disponible` | 503 | la base no responde |

Docker Compose usa `/salud` como healthcheck del backend (cada 30 s, 3
reintentos) y el frontend espera a que esté sano. La estación consulta `/salud`
cada 15 s y muestra "API conectada", "API conectada · modelos pendientes" o
"API no disponible".

## Registro de disponibilidad

```
cd backend
python -m benchmarks.monitor_disponibilidad --url http://127.0.0.1:8000/salud \
    --intervalo 60 --duracion 3600 --salida disponibilidad.csv
```

Cada sondeo guarda fecha UTC, código HTTP, estado y latencia. Un sondeo es
disponible si responde 200 (`ok` o `degradado`) en menos de 5 s. Criterio
RNF-03: disponibilidad mayor o igual al 95 % del periodo; el comando termina
con código 1 si no se cumple. Para el periodo de evaluación se recomienda
intervalo de 60 s durante toda la sesión de demostración.

Corrida de verificación del 2026-10-05 contra la API local: 12 sondeos cada
5 s, 12 disponibles, 100 %. No sustituye el registro del periodo de evaluación,
que el equipo debe ejecutar y anotar aquí.

## Logs mínimos

El middleware `notaryverify.acceso` registra una línea por solicitud con
método, ruta sin query, estado y duración, por ejemplo
`GET /salud 200 0.7ms`. No registra cabeceras, tokens, cuerpos, imágenes ni
documentos; `test_disponibilidad.py` lo verifica. El nivel se ajusta con
`NOTARYVERIFY_LOG_LEVEL`.

## Degradación comprensible

| Situación | Qué ve el operador |
| --- | --- |
| API caída | indicador rojo "API no disponible" y mensaje que pide verificar el backend |
| Modelos no descargados | indicador ámbar "modelos pendientes"; la primera captura requiere internet |
| Permiso de cámara denegado | motivo y opción de subir una fotografía |
| Sin cámara / cámara ocupada / origen inseguro | motivo específico (`NotFoundError`, `NotReadableError`, `SecurityError`) |
| Captura sin rostro o de baja calidad | motivo en la misma pantalla, sin cerrar la sesión |
