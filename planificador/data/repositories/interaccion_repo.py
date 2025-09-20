from planificador.data.db_manager import get_connection

class InteraccionRepository:

    @staticmethod
    def crear(id_cliente, fecha, tipo, descripcion=None,
              resultado="pendiente", id_contratacion=None,
              proxima_accion=None, fecha_proxima_accion=None, crear_recordatorio=0):
        with get_connection() as conn:
            cur = conn.execute("""
                INSERT INTO InteraccionCliente
                (id_cliente, id_contratacion, fecha, tipo, descripcion, resultado,
                 proxima_accion, fecha_proxima_accion, crear_recordatorio)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (id_cliente, id_contratacion, fecha, tipo, descripcion, resultado,
                  proxima_accion, fecha_proxima_accion, crear_recordatorio))
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def obtener_por_id(id_interaccion):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM InteraccionCliente WHERE id_interaccion=?", (id_interaccion,)).fetchone()

    @staticmethod
    def listar_por_cliente(id_cliente):
        with get_connection() as conn:
            return conn.execute("""
                SELECT * FROM InteraccionCliente
                WHERE id_cliente=?
                ORDER BY fecha DESC, created_at DESC
            """, (id_cliente,)).fetchall()

    @staticmethod
    def listar_pendientes():
        with get_connection() as conn:
            return conn.execute("""
                SELECT * FROM InteraccionCliente
                WHERE resultado='pendiente' OR (fecha_proxima_accion IS NOT NULL AND fecha_proxima_accion >= date('now'))
                ORDER BY fecha_proxima_accion
            """).fetchall()

    @staticmethod
    def actualizar(id_interaccion, **campos):
        if not campos:
            return
        sets = ", ".join(f"{k}=?" for k in campos)
        valores = list(campos.values()) + [id_interaccion]
        with get_connection() as conn:
            conn.execute(f"UPDATE InteraccionCliente SET {sets} WHERE id_interaccion=?", valores)
            conn.commit()

    @staticmethod
    def borrar(id_interaccion):
        with get_connection() as conn:
            conn.execute("DELETE FROM InteraccionCliente WHERE id_interaccion=?", (id_interaccion,))
            conn.commit()
