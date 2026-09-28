# Design

La expiración se evalúa en operación/consulta para mantener SQLite local sin
worker. El historial es exclusivo de Administrador y excluye rutas e imágenes.
No hay cambio de esquema: los campos ya persistidos se exponen de forma segura.
