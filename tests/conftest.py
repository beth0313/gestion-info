"""
conftest.py — Fixtures compartidos para toda la suite de pruebas.
"""

import pytest
from typing import Any

# Tipo alias reutilizable en los tests
UserDict = dict[str, Any]


@pytest.fixture
def sample_records() -> list[UserDict]:
    """Lista de usuarios de ejemplo, sin efectos secundarios entre tests."""
    return [
        {"id": "1", "name": "Ana Lopez",  "email": "ana@gmail.com"},
        {"id": "2", "name": "Carlos Diaz", "email": "carlos@hotmail.com"},
        {"id": "3", "name": "Maria Ruiz",  "email": "maria@empresa.co"},
    ]
