# Estrategia de pruebas

| Nivel | Evidencia | Método |
| --- | --- | --- |
| Unidad e integración backend | pytest | cd backend; python -m pytest -q |
| API | estado y OpenAPI | GET / y GET /docs |
| Frontend | estación, administración, credencial y auditoría | lista de humo manual |
| Contenedores | configuración y endpoints | docker compose config y docker compose up |
| Especificación | artefactos válidos | openspec validate cambio --strict |

## Evidencia inicial

El 2026-09-27, python -m pytest -q no inició porque faltaba el módulo sqlalchemy en el intérprete global. Se creó backend/.venv, se instalaron requirements.txt y la misma suite completó con 27 pruebas aprobadas y una advertencia de deprecación de Starlette. Las pruebas biométricas pueden requerir red en la primera ejecución.

La revisión de enlaces Markdown completó sin destinos locales faltantes. Docker
Compose resolvió correctamente con docker compose config. El 2026-09-28, con
Docker Desktop activo, se construyeron las imágenes e iniciaron los servicios;
los endpoints /, /openapi.json y el frontend en el puerto 5500 respondieron 200.

La prueba manual en navegador fue completada por el usuario: la cámara fue
detectada, se registró una identidad ficticia, se emitió una credencial y el
flujo terminó con Identidad verificada. La evidencia visual mostró credencial
válida, reconocimiento facial con confianza 0.54 y prueba de vida mediante giro
hacia la izquierda. No se registran datos personales en esta evidencia.
