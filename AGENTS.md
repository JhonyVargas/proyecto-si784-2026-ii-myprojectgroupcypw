# Guía de colaboración para NotaryVerify

## Antes de editar

1. Leer README.md, documentacion/indice.md y la sección aplicable.
2. Revisar cambios activos en openspec/changes y sus tareas.
3. Inspeccionar el código y pruebas cercanas antes de proponer modificaciones.

## Límites de arquitectura

- backend/app/api: interfaz HTTP; services: reglas y casos de uso; models: persistencia y esquemas; core: infraestructura.
- backend/tests contiene pruebas automatizadas.
- frontend es cliente estático; no introducir un framework sin propuesta aprobada.
- backend/data, cargas, modelos descargados, caches y entornos virtuales son runtime y no se versionan.
- documentacion/proyecto-si784-2026-ii-myprojectgroupcypw es una fuente histórica con Git propio: no borrar, reinicializar ni reescribir su historia.

## Seguridad y datos

No agregar datos reales de clientes, credenciales institucionales, tokens, documentos auténticos ni biometría sin consentimiento. Usar identidades, documentos y muestras ficticias. Conservar el aviso académico y no afirmar identificación legal.

## Calidad y cambios

Usar una rama focalizada con prefijo feat/, fix/, docs/ o chore/. Usar Conventional Commits, por ejemplo feat: validar credencial o docs: actualizar pruebas. Ejecutar las pruebas pertinentes; si no pueden ejecutarse, registrar comando, motivo y riesgo en la documentación o cambio.

Para cambios de modelo SQLAlchemy o persistencia, documentar compatibilidad, reinicio o migración, datos afectados y pruebas antes de editar. No cambiar el esquema solo mediante create_all sin una decisión explícita.

Actualizar documentación, OpenSpec y pruebas cuando cambien requisitos, API, seguridad, operación o comportamiento. Ejecutar como mínimo python -m pytest -q desde backend, las comprobaciones API necesarias y openspec validate para cambios OpenSpec.

No hacer commits, borrar informes ni mover el Git histórico salvo solicitud explícita del usuario.
