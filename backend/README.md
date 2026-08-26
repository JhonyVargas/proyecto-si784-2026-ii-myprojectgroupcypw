# NotaryVerify — Backend

API REST (FastAPI) del prototipo experimental de verificación multicapa de
identidad para trámites notariales, según lo especificado en `FD01`, `FD02`
y `FD03` (rama `documentos`).

Implementa: Simulador de Identidad, credenciales de prueba QR, reconocimiento
facial local (OpenCV), prueba de vida experimental (MediaPipe Face
Landmarker), motor de reglas de seguridad multicapa, integridad documental
(SHA-256), bitácora de auditoría con encadenamiento criptográfico y un
Simulador SID-Sunarp.

## Requisitos

- Python 3.11 o superior (probado con 3.14).
- Conexión a internet **la primera vez** que se ejecuta una verificación:
  el clasificador de detección facial y el modelo de MediaPipe se descargan
  automáticamente y se guardan en caché en `backend/data/modelos/`.

## Instalación

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
```

## Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

La API queda disponible en `http://127.0.0.1:8000`, con documentación
interactiva (Swagger) en `http://127.0.0.1:8000/docs`.

La base de datos SQLite (`backend/data/notaryverify.db`) y los archivos
subidos (referencias faciales, documentos) se crean automáticamente al
iniciar el servidor.

## Ejecutar las pruebas

```bash
pytest
```

Se incluyen pruebas unitarias del motor de reglas (RN-01), la bitácora de
auditoría con hash chain (RN-07), la integridad documental SHA-256 (RN-08),
el flujo de credenciales (RN-02 a RN-04) y el orquestador de verificación
multicapa completo (CU-03, RN-05). Dos pruebas de integración biométrica
descargan una imagen de referencia pública (`lena.jpg`) y se omiten
automáticamente si no hay conexión a internet.

## Estructura

```
backend/
  app/
    core/       # configuración y base de datos (SQLite)
    models/     # modelos SQLAlchemy y esquemas Pydantic
    services/   # lógica de dominio (RF-01 a RF-19, RN-01 a RN-10)
    api/        # routers de FastAPI
    main.py     # ensamblado de la aplicación
  tests/        # pruebas automatizadas (pytest)
  data/         # generado en tiempo de ejecución (no se versiona)
```

## Aviso académico

NotaryVerify es un prototipo experimental. No sustituye a Reniec, al
SID-Sunarp oficial ni a la firma digital oficial, y sus resultados **no**
tienen valor de identificación legal. Solo deben registrarse identidades
ficticias y datos biométricos de participantes voluntarios que hayan
otorgado su consentimiento expreso.
