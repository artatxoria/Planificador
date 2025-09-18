import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.json"

def cargar_config():
    """Carga y devuelve el diccionario de configuración desde config.json."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Prueba rápida
if __name__ == "__main__":
    config = cargar_config()
    print("Configuración cargada:", config["app"]["nombre"])
