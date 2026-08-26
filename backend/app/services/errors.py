"""Excepciones de dominio de NotaryVerify.

Se capturan en la capa API (app/api/*) y se traducen a códigos HTTP
apropiados, manteniendo la lógica de negocio independiente de FastAPI.
"""


class NotaryVerifyError(Exception):
    """Error base del dominio NotaryVerify."""


class ConsentimientoRequeridoError(NotaryVerifyError):
    """RN-03: no existe un consentimiento biométrico vigente para el participante."""


class IdentidadNoEncontradaError(NotaryVerifyError):
    pass


class CredencialNoRegistradaError(NotaryVerifyError):
    pass


class SesionNoEncontradaError(NotaryVerifyError):
    pass


class SesionNoVigenteError(NotaryVerifyError):
    """RN-10: la sesión ya no está en curso o expiró por inactividad."""


class RostroNoDetectadoError(NotaryVerifyError):
    pass


class TramiteNoHabilitadoError(NotaryVerifyError):
    """RN-06: solo se puede enviar un trámite si la sesión fue aprobada."""


class DocumentoNoEncontradoError(NotaryVerifyError):
    pass
