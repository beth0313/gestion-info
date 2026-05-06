"""
test_service.py — Pruebas de integracion para UserService.

Verifica el comportamiento del servicio como unidad: crear, listar,
actualizar, eliminar y los casos de error correspondientes.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from service import UserService
from exceptions import (
    DuplicateIDError,
    DuplicateEmailError,
    InvalidFieldError,
    UserNotFoundError,
)


@pytest.fixture
def service() -> UserService:
    """Servicio limpio para cada prueba."""
    return UserService()


@pytest.fixture
def service_with_user(service: UserService) -> UserService:
    """Servicio con un usuario ya cargado."""
    service.create_user("1", "Ana Lopez", "ana@example.com")
    return service


# ---------------------------------------------------------------------------
# create_user
# ---------------------------------------------------------------------------

class TestCreateUser:
    def test_create_valid_user(self, service):
        """Crear un usuario con datos validos lo agrega a la lista."""
        user = service.create_user("1", "Ana Lopez", "ana@example.com")
        assert user["id"] == "1"
        assert user["name"] == "Ana Lopez"
        assert user["email"] == "ana@example.com"
        assert len(service.list_records()) == 1

    def test_duplicate_id_raises(self, service_with_user):
        """Crear un usuario con ID duplicado lanza DuplicateIDError."""
        with pytest.raises(DuplicateIDError):
            service_with_user.create_user("1", "Otro Usuario", "otro@example.com")

    def test_duplicate_email_raises(self, service_with_user):
        """Crear un usuario con email duplicado lanza DuplicateEmailError."""
        with pytest.raises(DuplicateEmailError):
            service_with_user.create_user("2", "Otro Usuario", "ana@example.com")

    def test_invalid_name_raises(self, service):
        """Crear usuario con nombre de 1 caracter lanza InvalidFieldError."""
        with pytest.raises(InvalidFieldError):
            service.create_user("1", "X", "x@example.com")

    def test_invalid_email_raises(self, service):
        """Crear usuario con email malformado lanza InvalidFieldError."""
        with pytest.raises(InvalidFieldError):
            service.create_user("1", "Ana", "no-es-email")

    def test_empty_id_raises(self, service):
        """Crear usuario con ID vacio lanza InvalidFieldError."""
        with pytest.raises(InvalidFieldError):
            service.create_user("", "Ana", "ana@example.com")


# ---------------------------------------------------------------------------
# list_records
# ---------------------------------------------------------------------------

class TestListRecords:
    def test_empty_service_returns_empty_list(self, service):
        """Un servicio sin usuarios devuelve lista vacia."""
        assert service.list_records() == []

    def test_records_sorted_by_id(self, service):
        """list_records devuelve usuarios ordenados por ID ascendente."""
        service.create_user("3", "Carlos", "c@ex.com")
        service.create_user("1", "Ana", "a@ex.com")
        service.create_user("2", "Beto", "b@ex.com")
        ids = [u["id"] for u in service.list_records()]
        assert ids == ["1", "2", "3"]


# ---------------------------------------------------------------------------
# find_by_id
# ---------------------------------------------------------------------------

class TestFindById:
    def test_find_existing_user(self, service_with_user):
        """find_by_id retorna el usuario correcto."""
        user = service_with_user.find_by_id("1")
        assert user is not None
        assert user["name"] == "Ana Lopez"

    def test_find_nonexistent_returns_none(self, service):
        """find_by_id retorna None cuando el ID no existe."""
        assert service.find_by_id("999") is None


# ---------------------------------------------------------------------------
# update_user
# ---------------------------------------------------------------------------

class TestUpdateUser:
    def test_update_name(self, service_with_user):
        """Actualizar solo el nombre modifica unicamente ese campo."""
        service_with_user.update_user("1", name="Ana Maria")
        user = service_with_user.find_by_id("1")
        assert user["name"] == "Ana Maria"
        assert user["email"] == "ana@example.com"

    def test_update_email(self, service_with_user):
        """Actualizar solo el email modifica unicamente ese campo."""
        service_with_user.update_user("1", email="nueva@example.com")
        user = service_with_user.find_by_id("1")
        assert user["email"] == "nueva@example.com"

    def test_update_nonexistent_raises(self, service):
        """Actualizar un ID inexistente lanza UserNotFoundError."""
        with pytest.raises(UserNotFoundError):
            service.update_user("999", name="Nadie")

    def test_update_with_duplicate_email_raises(self, service):
        """Actualizar email a uno ya registrado lanza DuplicateEmailError."""
        service.create_user("1", "Ana", "ana@ex.com")
        service.create_user("2", "Beto", "beto@ex.com")
        with pytest.raises(DuplicateEmailError):
            service.update_user("2", email="ana@ex.com")

    def test_update_same_email_no_error(self, service_with_user):
        """Actualizar al mismo email actual no lanza ninguna excepcion."""
        service_with_user.update_user("1", email="ana@example.com")

    def test_update_empty_name_skipped(self, service_with_user):
        """Pasar name=None no debe modificar el nombre."""
        service_with_user.update_user("1", name=None)
        user = service_with_user.find_by_id("1")
        assert user["name"] == "Ana Lopez"


# ---------------------------------------------------------------------------
# delete_user
# ---------------------------------------------------------------------------

class TestDeleteUser:
    def test_delete_existing_user(self, service_with_user):
        """Eliminar un usuario existente lo remueve de la lista."""
        service_with_user.delete_user("1")
        assert service_with_user.list_records() == []

    def test_delete_nonexistent_raises(self, service):
        """Eliminar un ID inexistente lanza UserNotFoundError."""
        with pytest.raises(UserNotFoundError):
            service.delete_user("999")

    def test_delete_frees_email_for_reuse(self, service_with_user):
        """Tras eliminar un usuario su email queda disponible."""
        service_with_user.delete_user("1")
        # No debe lanzar DuplicateEmailError
        service_with_user.create_user("2", "Nuevo", "ana@example.com")
        assert service_with_user.find_by_id("2") is not None

    def test_delete_returns_deleted_user(self, service_with_user):
        """delete_user retorna el dict del usuario eliminado."""
        deleted = service_with_user.delete_user("1")
        assert deleted["id"] == "1"
