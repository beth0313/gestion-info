import json
import os

FILE_PATH = "data/records.json"

def load_data():
    try:
        if not os.path.exists(FILE_PATH):
            return []

        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:
        print("Archivo dañado. Iniciando vacío.")
        return []

def save_data(data):
    os.makedirs("data", exist_ok=True)

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)