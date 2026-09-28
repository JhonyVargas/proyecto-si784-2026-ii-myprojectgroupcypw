# Design

La imagen pendiente se conserva únicamente como archivo runtime hasta la
decisión. La aprobación usa reemplazo atómico sobre la referencia activa y el
rechazo elimina el archivo pendiente. La tabla aditiva es compatible con SQLite
existente; auditoría registra metadatos de decisión, nunca imágenes ni rutas.
