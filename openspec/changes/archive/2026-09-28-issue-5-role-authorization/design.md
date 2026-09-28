# Design

`require_roles` resuelve primero el token válido y luego compara el rol. La
administración de padrón, credenciales y auditoría requiere Administrador; el
flujo de verificación admite Operador o Administrador. La interfaz es una ayuda
de visibilidad, no un control de seguridad: la API siempre vuelve a validar.
