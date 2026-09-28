# Proposal

## Why

NotaryVerify ya contiene un prototipo funcional de verificación multicapa, pero
carece de una base de repositorio única que haga explícitos su alcance académico,
arquitectura, operación, calidad y forma de colaboración. La documentación actual
está separada y existe además como repositorio Git anidado, lo que dificulta la
trazabilidad y el desarrollo sostenido del proyecto universitario.

## What Changes

- Incorporar una línea de documentación versionada y navegable para el contexto,
  requisitos, arquitectura, planificación y calidad de NotaryVerify.
- Establecer una guía de colaboración para personas y agentes mediante un
  `AGENTS.md` raíz, con límites de privacidad biométrica, reglas para cambios de
  base de datos, pruebas, documentación, ramas y commits.
- Definir una estructura objetivo que conserve el backend FastAPI, el frontend
  estático y las pruebas existentes, eliminando la ambigüedad entre el panel
  legado y el panel actual durante una migración controlada.
- Definir configuración reproducible: ejemplos de variables de entorno y
  contenedores de desarrollo para la aplicación ya existente, sin sustituir sus
  tecnologías ni conectarla a servicios institucionales reales.
- Definir criterios de finalización, validación y trazabilidad para el bootstrap
  y para los cambios posteriores.

## Capabilities

### New Capabilities

- `repository-bootstrap`: estructura, documentación y configuración mínima que
  permiten comprender, ejecutar y mantener el prototipo sin alterar su dominio.
- `development-governance`: reglas verificables de colaboración, calidad y
  trazabilidad que deben seguir quienes modifiquen NotaryVerify.

### Modified Capabilities

Ninguna. No existen especificaciones OpenSpec previas y esta propuesta no cambia
el comportamiento funcional del prototipo.

## Impact

- Artefactos de repositorio previstos para la fase de aplicación: `README.md`,
  `AGENTS.md`, `documentacion/`, `.env.example`, `docker-compose.yml`,
  `.gitignore` y archivos de apoyo estrictamente necesarios.
- Se preservarán `backend/` (FastAPI, SQLAlchemy, SQLite y pytest), `frontend/`
  (HTML/CSS/JavaScript) y sus pruebas; no se crearán ni reescribirán productos de
  SocialAI Manager.
- La carpeta actual `Documentacion/` y su Git anidado requerirán una decisión de
  migración antes de cualquier movimiento, para no perder informes académicos.
- No se incorporan servicios reales de Reniec, SID-Sunarp, firma digital, datos
  personales reales ni biometría no consentida.
