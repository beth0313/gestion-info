"""
integration.py — Modulo 5/6: Integracion con pandas.

Responsabilidad: transformar la lista de usuarios en estructuras
de pandas para exportar, filtrar y generar reportes.
No contiene logica de negocio ni interaccion con el usuario.

Uso de *args / **kwargs:
  build_dataframe(*fields, records=...)  -- columnas a incluir
  filter_records(df, **criteria)         -- criterios de busqueda dinamicos
  export_csv(records, *fields, **kwargs) -- opciones de pandas.to_csv
"""

import os
from datetime import datetime
from typing import Any, Optional

import pandas as pd
import pandas.api.types as pat

# Ruta de salida por defecto (relativa a src/)
_DEFAULT_EXPORT = "data/reporte_usuarios.csv"

UserDict = dict[str, Any]


def build_dataframe(*fields: str, records: Optional[list[UserDict]] = None) -> pd.DataFrame:
    """
    Construye un DataFrame a partir de la lista de usuarios.

    Args:
        *fields:  Nombres de columnas a conservar. Si se omite, incluye todas.
        records:  Lista de dicts con datos de usuarios.

    Returns:
        DataFrame con los registros. Vacio si records es None o [].
    """
    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    if fields:
        valid = [f for f in fields if f in df.columns]
        if valid:
            df = df[valid]

    return df


def filter_records(df: pd.DataFrame, **criteria: str) -> pd.DataFrame:
    """
    Filtra un DataFrame por coincidencias de subcadena (case-insensitive).

    Args:
        df:         DataFrame de entrada.
        **criteria: Pares campo=valor. Se aplican todos (AND logico).
                    Ejemplo: filter_records(df, name="ana", email="gmail")

    Returns:
        DataFrame filtrado. Devuelve el original vacio si df ya es vacio.
    """
    if df.empty:
        return df

    result = df.copy()
    for field, value in criteria.items():
        if field not in result.columns:
            print(f"  [!] Campo '{field}' no existe, se ignora.")
            continue
        # pat.is_string_dtype cubre tanto 'object' como pandas StringDtype
        if pat.is_string_dtype(result[field]):
            mask = (
                result[field]
                .astype(str)
                .str.lower()
                .str.contains(str(value).lower(), na=False, regex=False)
            )
            result = result[mask]
        else:
            result = result[result[field] == value]

    return result


def export_csv(
    records: list[UserDict],
    *fields: str,
    filepath: str = _DEFAULT_EXPORT,
    **kwargs: Any,
) -> Optional[str]:
    """
    Exporta registros a un archivo CSV.

    Args:
        records:   Lista de usuarios a exportar.
        *fields:   Columnas a incluir (vacio = todas).
        filepath:  Ruta del CSV resultante.
        **kwargs:  Opciones extra para pandas.DataFrame.to_csv()
                   Ej: sep=";", encoding="utf-16"

    Returns:
        Ruta absoluta del CSV generado, o None si no hay registros.
    """
    if not records:
        print("  No hay registros para exportar.")
        return None

    df = build_dataframe(*fields, records=records)
    parent = os.path.dirname(filepath)
    if parent:
        os.makedirs(parent, exist_ok=True)

    opts: dict[str, Any] = {"index": False, "encoding": "utf-8"}
    opts.update(kwargs)
    df.to_csv(filepath, **opts)

    abs_path = os.path.abspath(filepath)
    print(f"  Exportado -> {abs_path}")
    print(f"  Registros: {len(df)}  |  Columnas: {list(df.columns)}")
    return abs_path


def generate_report(records: list[UserDict]) -> None:
    """
    Muestra en consola un reporte estadistico de los usuarios.

    Incluye: total de registros, dominios de email mas frecuentes
    y tabla ordenada por ID.

    Args:
        records: Lista de usuarios.
    """
    if not records:
        print("  No hay registros para reportar.")
        return

    df = build_dataframe(records=records)

    print("\n" + "=" * 50)
    print("         REPORTE DE USUARIOS")
    print(f"  Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    print(f"\n  Total de registros: {len(df)}")

    if "email" in df.columns:
        work = df.copy()
        work["dominio"] = work["email"].astype(str).str.split("@").str[-1]
        freq = work["dominio"].value_counts()
        print("\n  Dominios mas frecuentes:")
        for domain, count in freq.items():
            print(f"    {domain:<30} {count} usuario(s)")

    print("\n  Tabla (ordenada por ID):")
    sorted_df = df.sort_values("id").reset_index(drop=True)
    visible = [c for c in ["id", "name", "email"] if c in sorted_df.columns]
    print(sorted_df[visible].to_string(index=False))
    print("=" * 50)


def search_and_display(records: list[UserDict], **criteria: str) -> None:
    """
    Filtra registros con **criteria y muestra el resultado en consola.

    Args:
        records:    Lista de usuarios.
        **criteria: Pares campo=valor a buscar.
                    Ejemplo: search_and_display(records, email="gmail")
    """
    if not records:
        print("  No hay registros disponibles.")
        return

    df = build_dataframe(records=records)
    result = filter_records(df, **criteria)

    if result.empty:
        print("  No se encontraron registros con ese criterio.")
        return

    print(f"\n  Resultados ({len(result)} encontrado(s)):")
    visible = [c for c in ["id", "name", "email"] if c in result.columns]
    print(result[visible].to_string(index=False))
