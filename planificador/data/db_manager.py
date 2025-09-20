import sqlite3
from pathlib import Path

# Ruta al archivo de base de datos
DB_PATH = Path(__file__).resolve().parents[2] / "planificador.db"
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "data" / "schema.sql"


def get_connection():
    """
    Devuelve una conexión SQLite con foreign_keys activado.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acceder a columnas por nombre
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(force: bool = False):
    """
    Inicializa la base de datos ejecutando el script schema.sql.
    Si force=True, elimina primero la base de datos existente.
    """
    if force and DB_PATH.exists():
        DB_PATH.unlink()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()


if __name__ == "__main__":
    print(f"Inicializando la base de datos en: {DB_PATH}")
    init_db(force=True)
    print("Base de datos inicializada correctamente.")
