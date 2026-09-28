# Design

El frontend mantiene una única sesión de operador en `sessionStorage`, pero la
API continúa siendo el control de seguridad. Los códigos HTTP se traducen en
mensajes accionables y el flujo se puede reiniciar sin inferir aprobación de la
credencial.
