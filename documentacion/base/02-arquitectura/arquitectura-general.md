# Arquitectura general

El navegador y la estación consumen por HTTP el frontend estático. El frontend llama a FastAPI, que ensambla routers, servicios de dominio, SQLAlchemy con SQLite local, OpenCV/MediaPipe y datos runtime.

backend/app/api recibe HTTP. services aplica casos de uso y reglas. models mantiene entidades SQLAlchemy y esquemas Pydantic. core inicializa persistencia. El frontend captura datos, llama a la API y presenta resultados; no toma decisiones de verificación. Los simuladores son parte del backend y nunca servicios oficiales.
