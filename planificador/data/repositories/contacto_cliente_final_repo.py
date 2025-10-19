from planificador.data.db_manager import get_connection

class ContactoClienteFinalRepository:

    @staticmethod
    def crear(id_cliente_final, nombre, telefono=None, email=None, rol="encargado_formacion", notas=None):
        with get_connection() as conn:
            cur = conn.execute("""
                INSERT INTO ContactoClienteFinal (id_cliente_final, nombre, telefono, email, rol, notas)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (id_cliente_final, nombre, telefono, email, rol, notas))
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def obtener_por_id(id_contacto_final):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM ContactoClienteFinal WHERE id_contacto_final=?", (id_contacto_final,)).fetchone()

    @staticmethod
    def listar_por_cliente_final(id_cliente_final):
        with get_connection() as conn:
            return conn.execute("""
                SELECT * FROM ContactoClienteFinal
                WHERE id_cliente_final=?
                ORDER BY nombre
            """, (id_cliente_final,)).fetchall()

    @staticmethod
    def actualizar(id_contacto_final, **campos):
        if not campos:
            return
        sets = ", ".join(f"{k}=?" for k in campos)
        valores = list(campos.values()) + [id_contacto_final]
        with get_connection() as conn:
            conn.execute(f"UPDATE ContactoClienteFinal SET {sets} WHERE id_contacto_final=?", valores)
            conn.commit()

    @staticmethod
    def borrar(id_contacto_final):
        with get_connection() as conn:
            conn.execute("DELETE FROM ContactoClienteFinal WHERE id_contacto_final=?", (id_contacto_final,))
            conn.commit()
