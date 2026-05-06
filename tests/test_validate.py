"""
test_validate.py — Pruebas unitarias para el modulo validate.

Cubre todos los caminos felices y los casos de error de cada
funcion de validacion.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from validate import validate_id, validate_name, validate_email
from exceptions import DuplicateIDError, DuplicateEmailError, InvalidFieldError


# ---------------------------------------------------------------------------
# validate_id
# ---------------------------------------------------------------------------

class TestValidateId:
    def test_valid_id_passes(self):
        """Un ID no vacio y no duplicado debe pasar sin errores."""
        validate_id("42", set())

    def test_empty_id_raises(self):
        """Un ID vacio debe lanzar InvalidFieldError."""
        with pytest.raises(InvalidFieldError):
            validate_id("", set())

    def test_whitespace_only_id_raises(self):
        """Un ID con solo espacios debe lanzar InvalidFieldError."""
        with pytest.raises(InvalidFieldError):
            validate_id("   ", set())

    def test_duplicate_id_raises(self):
        """Un ID ya existente debe lanzar DuplicateIDError."""
        with pytest.raises(DuplicateIDError):
            validate_id("1", {"1", "2", "3"})

    def test_unique_id_in_nonempty_set_passes(self):
        """Un ID nuevo en un conjunto no vacio debe pasar."""
        validate_id("99", {"1", "2", "3"})  # sin excepcion


# ---------------------------------------------------------------------------
# validate_name
# ---------------------------------------------------------------------------

class TestValidateName:
    def test_valid_name_passes(self):
        """Un nombre con 2+ caracteres debe pasar."""
        validate_name("Ana")

    def test_single_char_name_raises(self):
        """Un nombre de 1 caracter debe lanzar InvalidFieldError."""
        with pytest.raises(InvalidFieldError):
            validate_name("A")

    def test_empty_name_raises(self):
        """Nombre vacio debe lanzar InvalidFieldError."""
        with pytest.raises(InvalidFieldError):
            validate_name("")

    def test_whitespace_name_raises(self):
        """Nombre con solo espacios debe lanzar InvalidFieldError."""
        with pytest.raises(InvalidFieldError):
            validate_name("  ")

    def test_two_char_name_passes(self):
        """Exactamente 2 caracteres es el minimo valido."""
        validate_name("Jo")

    def test_name_with_spaces_and_valid_length(self):
        """Nombre con espacios internos y longitud suficiente debe pasar."""
        validate_name("Ana Maria")


# ---------------------------------------------------------------------------
# validate_email
# ---------------------------------------------------------------------------

class TestValidateEmail:
    def test_valid_email_passes(self):
        """Email con formato correcto y no duplicado debe pasar."""
        validate_email("user@example.com", set())

    def test_invalid_format_raises(self):
        """Email sin @ debe lanzar InvalidFieldError."""
        with pytest.raises(InvalidFieldError):
            validate_email("not-an-email", set())

    def test_missing_domain_raises(self):
        """Email sin dominio debe lanzar InvalidFieldError."""
        with pytest.raises(InvalidFieldError):
            validate_email("user@", set())

    def test_missing_extension_raises(self):
        """Email sin extension (.com etc.) debe lanzar InvalidFieldError."""
        with pytest.raises(InvalidFieldError):
            validate_email("user@domain", set())

    def test_duplicate_email_raises(self):
        """Email ya registrado debe lanzar DuplicateEmailError."""
        with pytest.raises(DuplicateEmailError):
            validate_email("taken@example.com", {"taken@example.com"})

    def test_empty_email_raises(self):
        """Email vacio debe lanzar InvalidFieldError."""
        with pytest.raises(InvalidFieldError):
            validate_email("", set())

    def test_subdomain_email_passes(self):
        """Email con subdominio debe pasar la validacion."""
        validate_email("user@mail.company.co", set())
