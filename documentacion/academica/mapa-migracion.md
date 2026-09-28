# Mapa de preservación y migración

## Línea base — 2026-09-27

El repositorio principal registraba `Documentacion/proyecto-si784-2026-ii-myprojectgroupcypw` como gitlink. El contenido es un repositorio Git independiente en la rama `documentos`; no existe una entrada correspondiente en `.gitmodules`. Se realizó únicamente el renombrado reversible de `Documentacion/` a `documentacion/`; los archivos y el directorio `.git` interno permanecen intactos.

| Material original | Tratamiento | Estado |
| --- | --- | --- |
| `README.md` histórico | Fuente del alcance; enlazado desde índices canónicos | Conservado |
| `FD01-Informe-Factibilidad.md` y DOCX | Fuente académica de factibilidad | Conservado |
| `FD02-Informe-Vision.md` y DOCX | Fuente de visión, actores y alcance | Conservado |
| `FD03-Informe-SRS.md` y DOCX | Fuente de requisitos, reglas y casos de uso | Conservado |
| `FD04` a `FD06` DOCX | Entregables académicos | Conservados |
| `media/logo-upt.png` | Recurso institucional | Conservado |
| Repositorio Git interno | Historia de los informes | Conservado; decisión futura |
| `frontend/index.html`, `app.js`, `styles.css` | Panel anterior | Se conservará en `frontend/legacy-baseline/` al consolidar |
| `frontend/app/*` | Panel con estación, administración, credenciales y auditoría | Promovido mediante copia a la raíz; fuente conservada |

La comprobación de contenido confirmó que la entrada canónica contiene estación,
administración, credenciales y auditoría. El panel anterior se conserva en
`frontend/legacy-baseline/`; no se eliminará hasta que una revisión manual con
navegador y cámara esté disponible.

No se eliminó material histórico. Cualquier absorción del repositorio interno o eliminación posterior requiere una propuesta y aprobación explícitas.
