from planificador.data.db_manager import get_connection

class ContratacionRepository:

    @staticmethod
    def crear(id_cliente, id_formacion_base, expediente, precio_hora=None, horas_previstas=None,
              modalidad=None, direccion=None, enlace_vc=None, persona_responsable=None,
              telefono_responsable=None, email_responsable=None,
              fecha_inicio_prevista=None, fecha_fin_prevista=None, observaciones=None,
              estado="tentativo", prioridad="media"):
        with get_connection() as conn:
            cur = conn.execute("""
                INSERT INTO ContratacionClienteFormacion
                (id_cliente, id_formacion_base, expediente, precio_hora, horas_previstas, modalidad,
                 direccion, enlace_vc, persona_responsable, telefono_responsable, email_responsable,
                 fecha_inicio_prevista, fecha_fin_prevista, observaciones, estado, prioridad)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (id_cliente, id_formacion_base, expediente, precio_hora, horas_previstas, modalidad,
                  direccion, enlace_vc, persona_responsable, telefono_responsable, email_responsable,
                  fecha_inicio_prevista, fecha_fin_prevista, observaciones, estado, prioridad))
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def obtener_por_id(id_contratacion):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM ContratacionClienteFormacion WHERE id_contratacion=?", (id_contratacion,)).fetchone()

    @staticmethod
    def listar():
        with get_connection() as conn:
            return conn.execute("""
                SELECT ccf.*, cli.empresa, fb.nombre AS formacion
                FROM ContratacionClienteFormacion ccf
                JOIN Cliente cli ON ccf.id_cliente = cli.id_cliente
                JOIN FormacionBase fb ON ccf.id_formacion_base = fb.id_formacion_base
                ORDER BY fecha_inicio_prevista DESC
            """).fetchall()

    @staticmethod
    def actualizar(id_contratacion, **campos):
        if not campos:
            return
        sets = ", ".join(f"{k}=?" for k in campos)
        valores = list(campos.values()) + [id_contratacion]
        with get_connection() as conn:
            conn.execute(f"UPDATE ContratacionClienteFormacion SET {sets} WHERE id_contratacion=?", valores)
            conn.commit()

    @staticmethod
    def borrar(id_contratacion):
        with get_connection() as conn:
            conn.execute("DELETE FROM ContratacionClienteFormacion WHERE id_contratacion=?", (id_contratacion,))
            conn.commit()
