"""Catálogos de estados y resultados usados en todo el dominio de NotaryVerify.

Los valores replican textualmente los resultados definidos en el FD01
(Informe de Factibilidad) y el FD02 (Documento de Visión) del proyecto.
"""


class EstadoIdentidad:
    ACTIVA = "ACTIVA"
    BLOQUEADA = "BLOQUEADA"


class TipoCredencial:
    QR = "QR"
    RFID = "RFID"


class EstadoCredencial:
    ACTIVA = "ACTIVA"
    REVOCADA = "REVOCADA"


class EstadoSesion:
    EN_CURSO = "EN_CURSO"
    COMPLETADA = "COMPLETADA"
    EXPIRADA = "EXPIRADA"


class ResultadoVerificacion:
    IDENTIDAD_VERIFICADA = "IDENTIDAD_VERIFICADA"
    VERIFICACION_RECHAZADA = "VERIFICACION_RECHAZADA"
    ROSTRO_NO_COINCIDENTE = "ROSTRO_NO_COINCIDENTE"
    PRUEBA_DE_VIDA_FALLIDA = "PRUEBA_DE_VIDA_FALLIDA"
    CREDENCIAL_NO_REGISTRADA = "CREDENCIAL_NO_REGISTRADA"
    CREDENCIAL_REVOCADA = "CREDENCIAL_REVOCADA"
    MULTIPLES_INTENTOS_FALLIDOS = "MULTIPLES_INTENTOS_FALLIDOS"
    REQUIERE_REVISION = "VERIFICACION_REQUIERE_REVISION"


class RolUsuario:
    OPERADOR = "OPERADOR"
    ADMINISTRADOR = "ADMINISTRADOR"


class EstadoTramite:
    ENVIADO = "ENVIADO"
    RECHAZADO = "RECHAZADO"
    ERROR_SERVICIO = "ERROR_SERVICIO"
    TIEMPO_AGOTADO = "TIEMPO_AGOTADO"


class AccionPruebaVida:
    PARPADEO = "PARPADEO"
    GIRO_IZQUIERDA = "GIRO_IZQUIERDA"
    GIRO_DERECHA = "GIRO_DERECHA"
