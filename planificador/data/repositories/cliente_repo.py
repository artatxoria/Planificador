from planificador.data.db_manager import get_connection

class ClienteRepository:

    @staticmethod
    def crear(empresa, cif, persona_contacto=None, telefono=None, email=None,
              direccion=None, notas=None, color_hex="#377eb8"):
        with get_connection() as conn:
            cur = conn.execute("""
                INSERT INTO Cliente (empresa, persona_contacto, telefono, email, direccion, cif, notas, color_hex)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (empresa, persona_contacto, telefono, email, direccion, cif, notas, color_hex))
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def obtener_por_id(id_cliente):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM Cliente WHERE id_cliente=?", (id_cliente,)).fetchone()

    @staticmethod
    def listar():
        with get_connection() as conn:
            return conn.execute("SELECT * FROM Cliente ORDER BY empresa").fetchall()

    @staticmethod
    def actualizar(id_cliente, **campos):
        if not campos:
            return
        sets = ", ".join(f"{k}=?" for k in campos)
        valores = list(campos.values()) + [id_cliente]
        with get_connection() as conn:
            conn.execute(f"UPDATE Cliente SET {sets} WHERE id_cliente=?", valores)
            conn.commit()

    @staticmethod
    def borrar(id_cliente):
        with get_connection() as conn:
            conn.execute("DELETE FROM Cliente WHERE id_cliente=?", (id_cliente,))
            conn.commit()
