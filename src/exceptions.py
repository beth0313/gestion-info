"""
exceptions.py — Excepciones de dominio del sistema gestion-info.

Centraliza todos los errores propios de la aplicacion para que
el resto del codigo pueda capturarlos de forma especifica y consistente,
sin depender de ValueError generico.
"""


class AppError(Exception):
    """Clase base para todos los errores de la aplicacion."""


class DuplicateIDError(AppError):
    """Se intenta crear un usuario con un ID que ya existe."""


class DuplicateEmailError(AppError):
    """Se intenta registrar un email que ya esta en uso."""


class InvalidFieldError(AppError):
    """Un campo obligatorio esta vacio, es muy corto o tiene formato incorrecto."""


class UserNotFoundError(AppError):
    """Se solicita un usuario que no existe en el sistema."""
