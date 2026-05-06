"""
integration.py — Modulo 5: Integracion con pandas

Funcionalidades:
- Exportar registros a CSV
- Generar reporte estadistico en consola
- Filtrar/ordenar registros con DataFrame

Uso de *args / **kwargs:
- build_dataframe(*fields)    : elige que columnas incluir en el DataFrame
- filter_records(df, **crit)  : filtra por cualquier campo dinamicamente
- export_csv(*fields, **opts) : combina ambos y delega opciones a pandas
"""

import pandas as pd
import pandas.api.types as pat
import os
from datetime import datetime

EXPORT_PATH = "data/reporte_usuarios.csv"


def build_dataframe(*fields, records=None):
    """
    Construye un DataFrame a partir de los registros.

    *fields : columnas a incluir ("id", "name", "email").
              Si se omite, incluye todas las columnas disponibles.
    records : lista de dicts con los datos de usuarios.

    Retorna un pd.DataFrame.
    """
    if records is None:
        records = []

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    if fields:
        cols_validas = [f for f in fields if f in df.columns]
        if cols_validas:
            df = df[cols_validas]

    return df


def filter_records(df, **criteria):
    """
    Filtra un DataFrame segun criterios clave-valor.

    **criteria : pares campo=valor para filtrar.
                 Ejemplo: filter_records(df, name="ana")

    Retorna un DataFrame filtrado (insensible a mayusculas para strings).
    """
    if df.empty:
        return df

    result = df.copy()

    for campo, valor in criteria.items():
        if campo not in result.columns:
            print(f"  [!] Campo '{campo}' no existe, se ignora.")
            continue

        # Compatibilidad con pandas StringDtype y object
        if pat.is_string_dtype(result[campo]):
            result = result[
                result[campo].astype(str).str.lower().str.contains(
                    str(valor).lower(), na=False, regex=False
                )
            ]
        else:
            result = result[result[campo] == valor]

    return result


def export_csv(records, *fields, filepath=EXPORT_PATH, **kwargs):
    """
    Exporta los registros a un archivo CSV.

    records  : lista de dicts con usuarios.
    *fields  : columnas a incluir (vacio = todas).
    filepath : ruta de salida del CSV.
    **kwargs : opciones extra para pandas to_csv()
               Ej: sep=";", index=False
    """
    if not records:
        print("  No hay registros para exportar.")
        return None

    df = build_dataframe(*fields, records=records)

    directorio = os.path.dirname(filepath)
    if directorio:
        os.makedirs(directorio, exist_ok=True)

    csv_opts = {"index": False, "encoding": "utf-8"}
    csv_opts.update(kwargs)

    df.to_csv(filepath, **csv_opts)

    print(f"  Exportado -> {os.path.abspath(filepath)}")
    print(f"  Registros: {len(df)}  |  Columnas: {list(df.columns)}")
    return filepath


def generate_report(records):
    """
    Genera un reporte en consola con estadisticas basicas:
    - Total de registros
    - Dominios de email mas frecuentes
    - Tabla ordenada por ID
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
        df = df.copy()
        df["dominio"] = df["email"].astype(str).str.split("@").str[-1]
        conteo = df["dominio"].value_counts()
        print("\n  Dominios mas frecuentes:")
        for dominio, cuenta in conteo.items():
            print(f"    {dominio:<30} {cuenta} usuario(s)")

    print("\n  Tabla (ordenada por ID):")
    df_sorted = df.sort_values("id").reset_index(drop=True)
    cols = [c for c in ["id", "name", "email"] if c in df_sorted.columns]
    print(df_sorted[cols].to_string(index=False))
    print("=" * 50)


def search_and_display(records, **criteria):
    """
    Filtra registros con **kwargs y muestra el resultado en consola.

    Ejemplo: search_and_display(records, name="ana")
             search_and_display(records, email="gmail")
    """
    if not records:
        print("  No hay registros disponibles.")
        return

    df = build_dataframe(records=records)
    resultado = filter_records(df, **criteria)

    if resultado.empty:
        print("  No se encontraron registros con ese criterio.")
    else:
        print(f"\n  Resultados ({len(resultado)} encontrado(s)):")
        cols = [c for c in ["id", "name", "email"] if c in resultado.columns]
        print(resultado[cols].to_string(index=False))
