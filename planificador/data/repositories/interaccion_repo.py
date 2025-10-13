from planificador.data.db_manager import get_connection
from planificador.common.registro import get_logger

log = get_logger(__name__)

class InteraccionRepository:
    """
    Repositorio para gestionar la tabla InteraccionCliente.
    """

    @staticmethod
    def crear(id_cliente, fecha, tipo, descripcion=None,
              resultado="pendiente", proxima_accion=None,
              fecha_proxima_accion=None, crear_recordatorio=False):
        with get_connection() as conn:
            cur = conn.execute("""
                INSERT INTO InteraccionCliente (
                    id_cliente, fecha, tipo, descripcion, resultado,
                    proxima_accion, fecha_proxima_accion, crear_recordatorio
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (id_cliente, fecha, tipo, descripcion, resultado,
                  proxima_accion, fecha_proxima_accion, int(crear_recordatorio)))
            conn.commit()
            log.info(f"Nueva interacción creada para cliente {id_cliente} ({tipo})")
            return cur.lastrowid

    @staticmethod
    def obtener_por_id(id_interaccion):
        with get_connection() as conn:
            return conn.execute(
                "SELECT * FROM InteraccionCliente WHERE id_interaccion=?",
                (id_interaccion,)
            ).fetchone()

    @staticmethod
    def listar_por_cliente(id_cliente):
        with get_connection() as conn:
            return conn.execute(
                "SELECT * FROM InteraccionCliente WHERE id_cliente=? ORDER BY fecha DESC",
                (id_cliente,)
            ).fetchall()

    @staticmethod
    def listar_todas():
        with get_connection() as conn:
            return conn.execute(
                "SELECT * FROM InteraccionCliente ORDER BY fecha DESC"
            ).fetchall()

    @staticmethod
    def actualizar(id_interaccion, **campos):
        if not campos:
            return
        sets = ", ".join(f"{k}=?" for k in campos)
        valores = list(campos.values()) + [id_interaccion]
        with get_connection() as conn:
            conn.execute(f"UPDATE InteraccionCliente SET {sets} WHERE id_interaccion=?", valores)
            conn.commit()
            log.info(f"Interacción {id_interaccion} actualizada ({list(campos.keys())}).")

    @staticmethod
    def borrar(id_interaccion):
        with get_connection() as conn:
            conn.execute("DELETE FROM InteraccionCliente WHERE id_interaccion=?", (id_interaccion,))
            conn.commit()
            log.info(f"Interacción {id_interaccion} eliminada.")
