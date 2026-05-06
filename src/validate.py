"""
validate.py — Validaciones de campos de usuario.

Todas las reglas de negocio sobre formato y unicidad de campos
viven aqui. El resto del codigo llama estas funciones y captura
las excepciones de dominio definidas en exceptions.py.
"""

import re
from exceptions import DuplicateIDError, DuplicateEmailError, InvalidFieldError

# Patron de email: usuario@dominio.ext
_EMAIL_PATTERN = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")


def validate_id(user_id: str, existing_ids: set[str]) -> None:
    """
    Valida que el ID no este vacio y no este duplicado.

    Args:
        user_id:      Identificador propuesto para el nuevo usuario.
        existing_ids: Conjunto de IDs ya registrados en el sistema.

    Raises:
        InvalidFieldError:  Si user_id es una cadena vacia o solo espacios.
        DuplicateIDError:   Si user_id ya existe en existing_ids.
    """
    if not user_id or not user_id.strip():
        raise InvalidFieldError("El ID no puede estar vacio.")
    if user_id in existing_ids:
        raise DuplicateIDError(f"El ID '{user_id}' ya esta registrado.")


def validate_name(name: str) -> None:
    """
    Valida que el nombre tenga al menos 2 caracteres no espacios.

    Args:
        name: Nombre propuesto para el usuario.

    Raises:
        InvalidFieldError: Si el nombre es vacio o tiene menos de 2 caracteres.
    """
    if not name or len(name.strip()) < 2:
        raise InvalidFieldError("El nombre debe tener al menos 2 caracteres.")


def validate_email(email: str, existing_emails: set[str]) -> None:
    """
    Valida formato de email y que no este duplicado.

    Args:
        email:           Email propuesto para el usuario.
        existing_emails: Conjunto de emails ya registrados en el sistema.

    Raises:
        InvalidFieldError:    Si el email no cumple el patron basico.
        DuplicateEmailError:  Si el email ya esta en uso.
    """
    if not _EMAIL_PATTERN.match(email or ""):
        raise InvalidFieldError(f"El email '{email}' no tiene un formato valido.")
    if email in existing_emails:
        raise DuplicateEmailError(f"El email '{email}' ya esta registrado.")
