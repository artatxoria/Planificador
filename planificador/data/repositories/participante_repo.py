from planificador.data.db_manager import get_connection

class ParticipanteRepository:

    @staticmethod
    def crear(id_cliente_final, nombre, email=None, telefono=None, observaciones=None):
        with get_connection() as conn:
            cur = conn.execute("""
                INSERT INTO Participante (id_cliente_final, nombre, email, telefono, observaciones)
                VALUES (?, ?, ?, ?, ?)
            """, (id_cliente_final, nombre, email, telefono, observaciones))
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def obtener_por_id(id_participante):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM Participante WHERE id_participante=?", (id_participante,)).fetchone()

    @staticmethod
    def listar_por_cliente_final(id_cliente_final):
        with get_connection() as conn:
            return conn.execute("""
                SELECT * FROM Participante
                WHERE id_cliente_final=?
                ORDER BY nombre
            """, (id_cliente_final,)).fetchall()

    @staticmethod
    def actualizar(id_participante, **campos):
        if not campos:
            return
        sets = ", ".join(f"{k}=?" for k in campos)
        valores = list(campos.values()) + [id_participante]
        with get_connection() as conn:
            conn.execute(f"UPDATE Participante SET {sets} WHERE id_participante=?", valores)
            conn.commit()

    @staticmethod
    def borrar(id_participante):
        with get_connection() as conn:
            conn.execute("DELETE FROM Participante WHERE id_participante=?", (id_participante,))
            conn.commit()
