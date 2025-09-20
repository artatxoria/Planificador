from planificador.data.db_manager import get_connection

class FormacionBaseRepository:

    @staticmethod
    def crear(nombre, id_tema, descripcion=None, horas_referencia=None, nivel=None, contenido_base=None):
        with get_connection() as conn:
            cur = conn.execute("""
                INSERT INTO FormacionBase (nombre, descripcion, id_tema, horas_referencia, nivel, contenido_base)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nombre, descripcion, id_tema, horas_referencia, nivel, contenido_base))
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def obtener_por_id(id_formacion_base):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM FormacionBase WHERE id_formacion_base=?", (id_formacion_base,)).fetchone()

    @staticmethod
    def listar():
        with get_connection() as conn:
            return conn.execute("""
                SELECT fb.*, t.nombre AS tema
                FROM FormacionBase fb
                JOIN Tema t ON fb.id_tema = t.id_tema
                ORDER BY fb.nombre
            """).fetchall()

    @staticmethod
    def actualizar(id_formacion_base, **campos):
        if not campos:
            return
        sets = ", ".join(f"{k}=?" for k in campos)
        valores = list(campos.values()) + [id_formacion_base]
        with get_connection() as conn:
            conn.execute(f"UPDATE FormacionBase SET {sets} WHERE id_formacion_base=?", valores)
            conn.commit()

    @staticmethod
    def borrar(id_formacion_base):
        with get_connection() as conn:
            conn.execute("DELETE FROM FormacionBase WHERE id_formacion_base=?", (id_formacion_base,))
            conn.commit()
