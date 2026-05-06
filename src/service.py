"""
service.py — Logica de negocio para la gestion de usuarios.

UserService es la unica clase que coordina validaciones, mutaciones
en memoria y expone una API limpia al resto de la aplicacion.
No sabe nada de como se muestran datos ni como se persisten.
"""

from typing import Any, Optional
from validate import validate_id, validate_name, validate_email
from exceptions import UserNotFoundError

# Tipo alias para mayor legibilidad
UserDict = dict[str, Any]


class UserService:
    """Gestiona el ciclo de vida de los registros de usuario en memoria."""

    def __init__(self) -> None:
        self._users: list[UserDict] = []
        self._ids: set[str] = set()
        self._emails: set[str] = set()

    # ------------------------------------------------------------------
    # Inicializacion
    # ------------------------------------------------------------------

    def load_initial_data(self, records: list[UserDict]) -> None:
        """
        Carga registros iniciales desde una fuente externa (ej. archivo).

        Args:
            records: Lista de dicts con claves 'id', 'name', 'email'.
        """
        self._users = list(records)
        self._ids = {u["id"] for u in records}
        self._emails = {u["email"] for u in records}

    # ------------------------------------------------------------------
    # Consultas (sin efectos secundarios)
    # ------------------------------------------------------------------

    def list_records(self) -> list[UserDict]:
        """
        Devuelve todos los usuarios ordenados por ID de forma ascendente.

        Returns:
            Nueva lista ordenada; no modifica el estado interno.
        """
        return sorted(self._users, key=lambda u: u["id"])

    def find_by_id(self, user_id: str) -> Optional[UserDict]:
        """
        Busca un usuario por su ID.

        Args:
            user_id: ID a buscar.

        Returns:
            El dict del usuario si se encuentra, None en caso contrario.
        """
        return next((u for u in self._users if u["id"] == user_id), None)

    # ------------------------------------------------------------------
    # Mutaciones
    # ------------------------------------------------------------------

    def create_user(self, user_id: str, name: str, email: str) -> UserDict:
        """
        Crea y registra un nuevo usuario tras validar todos sus campos.

        Args:
            user_id: Identificador unico del usuario.
            name:    Nombre completo (min. 2 caracteres).
            email:   Correo electronico con formato valido y unico.

        Returns:
            El dict del usuario recien creado.

        Raises:
            InvalidFieldError:   Si algun campo no cumple el formato.
            DuplicateIDError:    Si el ID ya existe.
            DuplicateEmailError: Si el email ya esta registrado.
        """
        validate_id(user_id, self._ids)
        validate_name(name)
        validate_email(email, self._emails)

        user: UserDict = {"id": user_id, "name": name, "email": email}
        self._users.append(user)
        self._ids.add(user_id)
        self._emails.add(email)
        return user

    def update_user(
        self,
        user_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
    ) -> UserDict:
        """
        Actualiza el nombre y/o email de un usuario existente.

        Solo actualiza los campos que se pasen con un valor no vacio.

        Args:
            user_id: ID del usuario a modificar.
            name:    Nuevo nombre (opcional).
            email:   Nuevo email (opcional).

        Returns:
            El dict del usuario con los cambios aplicados.

        Raises:
            UserNotFoundError:   Si no existe un usuario con ese ID.
            InvalidFieldError:   Si el nuevo valor no cumple el formato.
            DuplicateEmailError: Si el nuevo email ya esta registrado.
        """
        user = self.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"No existe un usuario con ID '{user_id}'.")

        if name and name.strip():
            validate_name(name)
            user["name"] = name

        if email and email.strip():
            if email != user["email"]:
                validate_email(email, self._emails)
                self._emails.discard(user["email"])
                self._emails.add(email)
                user["email"] = email

        return user

    def delete_user(self, user_id: str) -> UserDict:
        """
        Elimina un usuario del sistema.

        Args:
            user_id: ID del usuario a eliminar.

        Returns:
            El dict del usuario eliminado.

        Raises:
            UserNotFoundError: Si no existe un usuario con ese ID.
        """
        user = self.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"No existe un usuario con ID '{user_id}'.")

        self._users.remove(user)
        self._ids.discard(user["id"])
        self._emails.discard(user["email"])
        return user
