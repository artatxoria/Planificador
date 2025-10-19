from planificador.data.db_manager import get_connection

class ClienteFinalRepository:

    @staticmethod
    def crear(empresa, persona_encargada=None, telefono_encargada=None,
              email_encargada=None, direccion=None, notas=None):
        with get_connection() as conn:
            cur = conn.execute("""
                INSERT INTO ClienteFinal (empresa, persona_encargada, telefono_encargada, email_encargada, direccion, notas)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (empresa, persona_encargada, telefono_encargada, email_encargada, direccion, notas))
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def obtener_por_id(id_cliente_final):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM ClienteFinal WHERE id_cliente_final=?", (id_cliente_final,)).fetchone()

    @staticmethod
    def listar():
        with get_connection() as conn:
            return conn.execute("SELECT * FROM ClienteFinal ORDER BY empresa").fetchall()

    @staticmethod
    def actualizar(id_cliente_final, **campos):
        if not campos:
            return
        sets = ", ".join(f"{k}=?" for k in campos)
        valores = list(campos.values()) + [id_cliente_final]
        with get_connection() as conn:
            conn.execute(f"UPDATE ClienteFinal SET {sets} WHERE id_cliente_final=?", valores)
            conn.commit()

    @staticmethod
    def borrar(id_cliente_final):
        with get_connection() as conn:
            conn.execute("DELETE FROM ClienteFinal WHERE id_cliente_final=?", (id_cliente_final,))
            conn.commit()
