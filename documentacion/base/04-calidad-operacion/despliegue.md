# Ejecución y despliegue local

## Nativo

Desde backend: crear un entorno virtual, activarlo, instalar requirements.txt y ejecutar uvicorn app.main:app --reload.

En otra terminal, desde frontend: python -m http.server 5500. Visitar http://127.0.0.1:5500; API y Swagger: http://127.0.0.1:8000 y http://127.0.0.1:8000/docs.

Compose ofrece el equivalente local cuando Docker esté disponible. El volumen de datos es de desarrollo y puede reiniciarse; nunca contiene información real. Detener servicios con Ctrl+C o docker compose down.
