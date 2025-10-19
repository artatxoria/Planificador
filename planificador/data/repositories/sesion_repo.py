from planificador.data.db_manager import get_connection
from planificador.common.registro import get_logger

log = get_logger(__name__)

class SesionRepository:
    """
    Repositorio de acceso a datos para la tabla Sesion.
    Permite crear, consultar, actualizar y eliminar sesiones de formación.
    """

    @staticmethod
    def crear(id_contratacion, fecha=None, hora_inicio=None, hora_fin=None,
              direccion=None, enlace_vc=None, estado="propuesta", notas=None):
        """
        Crea una nueva sesión. Permite registrar propuestas sin fecha ni hora aún definidas.
        """
        with get_connection() as conn:
            cur = conn.execute("""
                INSERT INTO Sesion (id_contratacion, fecha, hora_inicio, hora_fin,
                                    direccion, enlace_vc, estado, notas)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (id_contratacion, fecha, hora_inicio, hora_fin,
                  direccion, enlace_vc, estado, notas))
            conn.commit()

            log.info(
                f"Sesión creada: estado={estado}, contratación={id_contratacion}, "
                f"fecha={fecha or 'sin definir'}"
            )

            return cur.lastrowid

    @staticmethod
    def obtener_por_id(id_sesion):
        with get_connection() as conn:
            return conn.execute(
                "SELECT * FROM Sesion WHERE id_sesion=?",
                (id_sesion,)
            ).fetchone()

    @staticmethod
    def listar_por_contratacion(id_contratacion):
        with get_connection() as conn:
            return conn.execute(
                "SELECT * FROM Sesion WHERE id_contratacion=? ORDER BY fecha, hora_inicio",
                (id_contratacion,)
            ).fetchall()

    @staticmethod
    def listar_por_fecha(fecha):
        with get_connection() as conn:
            return conn.execute(
                "SELECT * FROM Sesion WHERE fecha=? ORDER BY hora_inicio",
                (fecha,)
            ).fetchall()

    @staticmethod
    def listar_todas():
        """
        Devuelve todas las sesiones registradas en la base de datos.
        """
        with get_connection() as conn:
            cur = conn.execute("""
                SELECT id_sesion, id_contratacion, fecha, hora_inicio, hora_fin,
                       direccion, enlace_vc, estado, notas
                FROM Sesion
                ORDER BY fecha ASC, hora_inicio ASC
            """)
            columnas = [c[0] for c in cur.description]
            return [dict(zip(columnas, fila)) for fila in cur.fetchall()]

    @staticmethod
    def actualizar(id_sesion, **campos):
        if not campos:
            return
        sets = ", ".join(f"{k}=?" for k in campos)
        valores = list(campos.values()) + [id_sesion]
        with get_connection() as conn:
            conn.execute(f"UPDATE Sesion SET {sets} WHERE id_sesion=?", valores)
            conn.commit()
            log.info(f"Sesión {id_sesion} actualizada: {campos}")

    @staticmethod
    def borrar(id_sesion):
        with get_connection() as conn:
            conn.execute("DELETE FROM Sesion WHERE id_sesion=?", (id_sesion,))
            conn.commit()
            log.info(f"Sesión {id_sesion} eliminada.")
