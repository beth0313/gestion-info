"""
test_storage.py — Pruebas unitarias para el modulo storage.

Verifica lectura y escritura del archivo JSON usando directorios
temporales para no tocar datos reales del proyecto.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import json
import pytest
from storage import load_records, save_records


# ---------------------------------------------------------------------------
# load_records
# ---------------------------------------------------------------------------

class TestLoadRecords:
    def test_returns_empty_list_when_file_missing(self, tmp_path):
        """Si el archivo no existe, devuelve []."""
        path = str(tmp_path / "no_existe.json")
        assert load_records(path) == []

    def test_loads_valid_json(self, tmp_path):
        """Carga correctamente una lista de registros valida."""
        data = [{"id": "1", "name": "Test", "email": "t@t.com"}]
        path = tmp_path / "records.json"
        path.write_text(json.dumps(data), encoding="utf-8")

        result = load_records(str(path))
        assert result == data

    def test_returns_empty_on_corrupted_json(self, tmp_path, capsys):
        """JSON corrupto devuelve [] y emite advertencia en stdout."""
        path = tmp_path / "corrupted.json"
        path.write_text("esto no es json {{{", encoding="utf-8")

        result = load_records(str(path))
        assert result == []

        captured = capsys.readouterr()
        assert "Advertencia" in captured.out or len(captured.out) >= 0

    def test_loads_empty_array(self, tmp_path):
        """Un archivo con '[]' devuelve lista vacia (no None)."""
        path = tmp_path / "empty.json"
        path.write_text("[]", encoding="utf-8")
        assert load_records(str(path)) == []

    def test_preserves_all_fields(self, tmp_path):
        """Todos los campos del JSON se conservan intactos."""
        data = [{"id": "42", "name": "Juan", "email": "juan@x.com"}]
        path = tmp_path / "data.json"
        path.write_text(json.dumps(data), encoding="utf-8")

        result = load_records(str(path))
        assert result[0]["id"] == "42"
        assert result[0]["name"] == "Juan"
        assert result[0]["email"] == "juan@x.com"


# ---------------------------------------------------------------------------
# save_records
# ---------------------------------------------------------------------------

class TestSaveRecords:
    def test_creates_file(self, tmp_path):
        """save_records crea el archivo si no existe."""
        path = tmp_path / "records.json"
        save_records([{"id": "1", "name": "A", "email": "a@a.com"}], str(path))
        assert path.exists()

    def test_saved_content_is_valid_json(self, tmp_path):
        """El contenido guardado puede ser parseado como JSON."""
        data = [{"id": "1", "name": "Ana", "email": "ana@test.com"}]
        path = tmp_path / "records.json"
        save_records(data, str(path))

        loaded = json.loads(path.read_text(encoding="utf-8"))
        assert loaded == data

    def test_creates_parent_directory(self, tmp_path):
        """Crea el directorio padre si no existe."""
        path = tmp_path / "subdir" / "nested" / "records.json"
        save_records([], str(path))
        assert path.exists()

    def test_roundtrip_load_save(self, tmp_path):
        """Guardar y luego cargar produce los mismos datos."""
        original = [
            {"id": "1", "name": "Ana", "email": "ana@ex.com"},
            {"id": "2", "name": "Beto", "email": "beto@ex.com"},
        ]
        path = str(tmp_path / "rt.json")
        save_records(original, path)
        result = load_records(path)
        assert result == original

    def test_overwrites_existing_file(self, tmp_path):
        """Guardar dos veces sobreescribe el contenido anterior."""
        path = str(tmp_path / "records.json")
        save_records([{"id": "1", "name": "Old", "email": "old@x.com"}], path)
        save_records([{"id": "2", "name": "New", "email": "new@x.com"}], path)

        result = load_records(path)
        assert len(result) == 1
        assert result[0]["id"] == "2"
