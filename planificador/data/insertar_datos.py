import sqlite3
from pathlib import Path

# Asume que db_manager.py y el archivo de datos están en un proyecto estructurado
# Ajusta estas rutas según la ubicación real de tus archivos
# Por ejemplo, si insert_data.sql está en el mismo directorio que este script
# y planificador.db está dos directorios arriba, como en db_manager.py

# Ruta al archivo de base de datos (ajusta si es necesario)
# Esta ruta debe ser la misma que la utilizada en db_manager.py para la base de datos
DB_PATH = Path(__file__).resolve().parents[2] / "planificador.db"
# Ruta al archivo SQL con los datos de inserción
INSERT_DATA_PATH = Path(__file__).resolve().parent / "datos.sql"

def get_connection():
    """
    Devuelve una conexión SQLite con foreign_keys activado.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acceder a columnas por nombre
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def insert_data():
    """
    Inserta los datos desde el script SQL en la base de datos.
    """
    if not DB_PATH.exists():
        print(f"Error: La base de datos no existe en {DB_PATH}. Asegúrate de que ha sido inicializada.")
        return

    print(f"Insertando datos en la base de datos: {DB_PATH}")
    print(f"Desde el archivo: {INSERT_DATA_PATH}")
    
    try:
        with get_connection() as conn:
            with open(INSERT_DATA_PATH, "r", encoding="utf-8") as f:
                sql_script = f.read()
                conn.executescript(sql_script)
            conn.commit()
        print("Datos insertados correctamente.")
    except sqlite3.Error as e:
        print(f"Error al insertar datos: {e}")

if __name__ == "__main__":
    insert_data()
