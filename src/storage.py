"""
storage.py — Capa de persistencia JSON.

Responsabilidad unica: leer y escribir la lista de usuarios en disco.
No contiene logica de negocio ni validaciones.

El nombre 'storage' reemplaza a 'file.py' para evitar colision con
el modulo estandar 'fileinput' y expresar mejor la intencion del modulo.
"""

import json
import os
from typing import Any

# Ruta por defecto, relativa al directorio de trabajo (src/)
_DEFAULT_PATH = "data/records.json"


def load_records(filepath: str = _DEFAULT_PATH) -> list[dict[str, Any]]:
    """
    Carga la lista de usuarios desde un archivo JSON.

    Si el archivo no existe devuelve una lista vacia.
    Si el JSON esta corrupto imprime una advertencia y devuelve lista vacia.

    Args:
        filepath: Ruta al archivo JSON. Por defecto 'data/records.json'.

    Returns:
        Lista de dicts con los datos de usuarios, o [] si no hay datos.
    """
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError:
        print(f"[Advertencia] El archivo '{filepath}' esta danado. Se inicia vacio.")
        return []


def save_records(
    records: list[dict[str, Any]],
    filepath: str = _DEFAULT_PATH,
) -> None:
    """
    Guarda la lista de usuarios en un archivo JSON.

    Crea el directorio padre si no existe.

    Args:
        records:  Lista de dicts a serializar.
        filepath: Ruta de destino. Por defecto 'data/records.json'.
    """
    parent = os.path.dirname(filepath)
    if parent:
        os.makedirs(parent, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as fh:
        json.dump(records, fh, indent=4, ensure_ascii=False)
