from planificador.data.db_manager import get_connection

class AdjuntoRepository:

    @staticmethod
    def crear(origen, id_origen, ruta_fichero, tipo=None, notas=None):
        with get_connection() as conn:
            cur = conn.execute("""
                INSERT INTO Adjunto (origen, id_origen, tipo, ruta_fichero, notas)
                VALUES (?, ?, ?, ?, ?)
            """, (origen, id_origen, tipo, ruta_fichero, notas))
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def obtener_por_id(id_adjunto):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM Adjunto WHERE id_adjunto=?", (id_adjunto,)).fetchone()

    @staticmethod
    def listar_por_origen(origen, id_origen):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM Adjunto WHERE origen=? AND id_origen=?", (origen, id_origen)).fetchall()

    @staticmethod
    def borrar(id_adjunto):
        with get_connection() as conn:
            conn.execute("DELETE FROM Adjunto WHERE id_adjunto=?", (id_adjunto,))
            conn.commit()
