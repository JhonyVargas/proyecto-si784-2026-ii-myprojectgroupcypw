# Design

Un manejador global mapea excepciones de dominio a una respuesta `detail` con
`code` estable y mensaje seguro. Los routers propagan las excepciones y no
duplican las traducciones.
