"""
test_integration.py — Pruebas para el modulo integration (pandas).

Verifica build_dataframe, filter_records, export_csv,
generate_report y search_and_display usando fixtures y
directorios temporales; sin tocar el sistema de archivos real.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
import pandas as pd
from integration import (
    build_dataframe,
    filter_records,
    export_csv,
    generate_report,
    search_and_display,
)


# ---------------------------------------------------------------------------
# build_dataframe
# ---------------------------------------------------------------------------

class TestBuildDataframe:
    def test_empty_records_returns_empty_df(self):
        """Sin registros devuelve DataFrame vacio."""
        df = build_dataframe(records=[])
        assert df.empty

    def test_none_records_returns_empty_df(self):
        """records=None devuelve DataFrame vacio."""
        df = build_dataframe(records=None)
        assert df.empty

    def test_all_columns_present(self, sample_records):
        """Con registros validos el DataFrame tiene las 3 columnas."""
        df = build_dataframe(records=sample_records)
        assert set(df.columns) == {"id", "name", "email"}
        assert len(df) == len(sample_records)

    def test_select_single_field(self, sample_records):
        """*fields filtra y deja solo la columna solicitada."""
        df = build_dataframe("email", records=sample_records)
        assert list(df.columns) == ["email"]

    def test_select_multiple_fields(self, sample_records):
        """*fields multiples conserva solo esas columnas, en ese orden."""
        df = build_dataframe("id", "name", records=sample_records)
        assert list(df.columns) == ["id", "name"]

    def test_nonexistent_field_ignored(self, sample_records):
        """Un campo inexistente en *fields se ignora sin error."""
        df = build_dataframe("id", "no_existe", records=sample_records)
        assert "id" in df.columns
        assert "no_existe" not in df.columns

    def test_row_count_matches_records(self, sample_records):
        """El numero de filas coincide con el numero de registros."""
        df = build_dataframe(records=sample_records)
        assert len(df) == 3


# ---------------------------------------------------------------------------
# filter_records
# ---------------------------------------------------------------------------

class TestFilterRecords:
    def test_empty_df_returns_empty(self):
        """Filtrar un DataFrame vacio devuelve DataFrame vacio."""
        df = pd.DataFrame()
        result = filter_records(df, name="ana")
        assert result.empty

    def test_filter_by_name_case_insensitive(self, sample_records):
        """El filtro de texto es insensible a mayusculas."""
        df = build_dataframe(records=sample_records)
        result = filter_records(df, name="ana")
        assert len(result) == 1
        assert "Ana Lopez" in result["name"].values

    def test_filter_by_email_domain(self, sample_records):
        """Filtrar por dominio de email retorna coincidencias parciales."""
        df = build_dataframe(records=sample_records)
        result = filter_records(df, email="gmail")
        assert len(result) == 1

    def test_filter_no_match_returns_empty(self, sample_records):
        """Criterio sin coincidencia devuelve DataFrame vacio."""
        df = build_dataframe(records=sample_records)
        result = filter_records(df, name="zzznoencontrado")
        assert result.empty

    def test_multiple_criteria_applied_as_and(self, sample_records):
        """Multiples criterios se aplican con logica AND."""
        df = build_dataframe(records=sample_records)
        # Solo 'ana' con gmail debe coincidir con ambos criterios
        result = filter_records(df, name="ana", email="gmail")
        assert len(result) == 1

    def test_nonexistent_field_prints_warning(self, sample_records, capsys):
        """Campo inexistente emite advertencia y no falla."""
        df = build_dataframe(records=sample_records)
        result = filter_records(df, campo_raro="valor")
        # Debe imprimir aviso
        captured = capsys.readouterr()
        assert "no existe" in captured.out
        # Y devolver el df sin filtrar
        assert len(result) == 3

    def test_filter_by_exact_id(self, sample_records):
        """Filtro por ID retorna el usuario correcto."""
        df = build_dataframe(records=sample_records)
        result = filter_records(df, id="2")
        assert len(result) == 1
        assert result.iloc[0]["name"] == "Carlos Diaz"


# ---------------------------------------------------------------------------
# export_csv
# ---------------------------------------------------------------------------

class TestExportCsv:
    def test_creates_csv_file(self, sample_records, tmp_path):
        """export_csv crea el archivo en la ruta indicada."""
        path = str(tmp_path / "out.csv")
        result = export_csv(sample_records, filepath=path)
        assert result == os.path.abspath(path)
        assert os.path.exists(path)

    def test_csv_has_correct_rows(self, sample_records, tmp_path):
        """El CSV tiene tantas filas de datos como registros."""
        path = str(tmp_path / "out.csv")
        export_csv(sample_records, filepath=path)
        import csv
        with open(path, encoding="utf-8") as f:
            rows = list(csv.reader(f))
        # 1 cabecera + N filas de datos
        assert len(rows) == len(sample_records) + 1

    def test_export_selected_columns(self, sample_records, tmp_path):
        """*fields limita las columnas del CSV exportado."""
        path = str(tmp_path / "partial.csv")
        export_csv(sample_records, "id", "name", filepath=path)
        import csv
        with open(path, encoding="utf-8") as f:
            header = next(csv.reader(f))
        assert header == ["id", "name"]

    def test_empty_records_returns_none(self, capsys):
        """Sin registros devuelve None y no crea archivo."""
        result = export_csv([])
        assert result is None

    def test_kwargs_passed_to_pandas(self, sample_records, tmp_path):
        """**kwargs extra (ej: sep) se pasan correctamente a to_csv."""
        path = str(tmp_path / "semicolon.csv")
        export_csv(sample_records, filepath=path, sep=";")
        content = open(path, encoding="utf-8").read()
        assert ";" in content


# ---------------------------------------------------------------------------
# generate_report  (prueba de salida en consola)
# ---------------------------------------------------------------------------

class TestGenerateReport:
    def test_empty_records_prints_message(self, capsys):
        """Sin registros imprime aviso de lista vacia."""
        generate_report([])
        out = capsys.readouterr().out
        assert "No hay" in out

    def test_report_shows_total(self, sample_records, capsys):
        """El reporte muestra el total de registros."""
        generate_report(sample_records)
        out = capsys.readouterr().out
        assert "3" in out

    def test_report_shows_domain(self, sample_records, capsys):
        """El reporte muestra al menos un dominio de email."""
        generate_report(sample_records)
        out = capsys.readouterr().out
        assert "gmail.com" in out

    def test_report_contains_header(self, sample_records, capsys):
        """El reporte incluye la cabecera 'REPORTE DE USUARIOS'."""
        generate_report(sample_records)
        out = capsys.readouterr().out
        assert "REPORTE" in out


# ---------------------------------------------------------------------------
# search_and_display
# ---------------------------------------------------------------------------

class TestSearchAndDisplay:
    def test_empty_records_prints_message(self, capsys):
        """Sin registros imprime aviso."""
        search_and_display([], name="ana")
        out = capsys.readouterr().out
        assert "No hay" in out

    def test_found_records_printed(self, sample_records, capsys):
        """Registros encontrados se imprimen en consola."""
        search_and_display(sample_records, name="ana")
        out = capsys.readouterr().out
        assert "Ana Lopez" in out

    def test_no_match_prints_message(self, sample_records, capsys):
        """Sin coincidencias imprime aviso apropiado."""
        search_and_display(sample_records, name="zzz")
        out = capsys.readouterr().out
        assert "No se encontraron" in out

    def test_result_count_in_output(self, sample_records, capsys):
        """La salida indica cuantos registros se encontraron."""
        search_and_display(sample_records, email="gmail")
        out = capsys.readouterr().out
        assert "1" in out
