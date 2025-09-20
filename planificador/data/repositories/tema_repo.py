from planificador.data.db_manager import get_connection

class TemaRepository:

    @staticmethod
    def crear(nombre, descripcion=None):
        with get_connection() as conn:
            cur = conn.execute("INSERT INTO Tema (nombre, descripcion) VALUES (?, ?)", (nombre, descripcion))
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def obtener_por_id(id_tema):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM Tema WHERE id_tema=?", (id_tema,)).fetchone()

    @staticmethod
    def listar():
        with get_connection() as conn:
            return conn.execute("SELECT * FROM Tema ORDER BY nombre").fetchall()

    @staticmethod
    def actualizar(id_tema, **campos):
        if not campos:
            return
        sets = ", ".join(f"{k}=?" for k in campos)
        valores = list(campos.values()) + [id_tema]
        with get_connection() as conn:
            conn.execute(f"UPDATE Tema SET {sets} WHERE id_tema=?", valores)
            conn.commit()

    @staticmethod
    def borrar(id_tema):
        with get_connection() as conn:
            conn.execute("DELETE FROM Tema WHERE id_tema=?", (id_tema,))
            conn.commit()
