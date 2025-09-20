from planificador.data.db_manager import get_connection

class SesionRepository:

    @staticmethod
    def crear(id_contratacion, fecha, hora_inicio, hora_fin,
              direccion=None, enlace_vc=None, estado="programada", notas=None):
        with get_connection() as conn:
            cur = conn.execute("""
                INSERT INTO Sesion (id_contratacion, fecha, hora_inicio, hora_fin, direccion, enlace_vc, estado, notas)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (id_contratacion, fecha, hora_inicio, hora_fin, direccion, enlace_vc, estado, notas))
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def obtener_por_id(id_sesion):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM Sesion WHERE id_sesion=?", (id_sesion,)).fetchone()

    @staticmethod
    def listar_por_contratacion(id_contratacion):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM Sesion WHERE id_contratacion=? ORDER BY fecha, hora_inicio", (id_contratacion,)).fetchall()

    @staticmethod
    def actualizar(id_sesion, **campos):
        if not campos:
            return
        sets = ", ".join(f"{k}=?" for k in campos)
        valores = list(campos.values()) + [id_sesion]
        with get_connection() as conn:
            conn.execute(f"UPDATE Sesion SET {sets} WHERE id_sesion=?", valores)
            conn.commit()

    @staticmethod
    def borrar(id_sesion):
        with get_connection() as conn:
            conn.execute("DELETE FROM Sesion WHERE id_sesion=?", (id_sesion,))
            conn.commit()
