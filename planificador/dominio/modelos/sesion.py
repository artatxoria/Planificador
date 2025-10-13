from datetime import datetime
from planificador.common.utilidades import a_minutos
from planificador.common.registro import get_logger

log = get_logger(__name__)

class Sesion:
    """
    Clase de dominio que representa una sesión individual dentro de una contratación.
    Incluye validación y registro de actividad.
    """

    def __init__(self, id_contratacion, fecha, hora_inicio, hora_fin,
                 direccion=None, enlace_vc=None, estado="programada",
                 notas=None, id_sesion=None, created_at=None):
        self.id_sesion = id_sesion
        self.id_contratacion = id_contratacion
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.direccion = direccion
        self.enlace_vc = enlace_vc
        self.estado = estado
        self.notas = notas
        self.created_at = created_at or datetime.now().isoformat()

        self._validar()
        log.info(f"Sesión creada: {self.fecha} {self.hora_inicio}-{self.hora_fin}, contratación={self.id_contratacion}, id={self.id_sesion or 'pendiente'}")

    def _validar(self):
        if not self.id_contratacion:
            log.error("Error al crear Sesion: falta 'id_contratacion'")
            raise ValueError("La sesión debe estar vinculada a una contratación")
        if not self.fecha:
            log.error("Error al crear Sesion: falta 'fecha'")
            raise ValueError("La sesión debe tener una fecha")
        if not self.hora_inicio or not self.hora_fin:
            log.error("Error al crear Sesion: faltan horas de inicio o fin")
            raise ValueError("La sesión debe tener hora de inicio y hora de fin")
        if self.hora_inicio >= self.hora_fin:
            log.error(f"Horas inválidas en Sesion {self.fecha}: inicio={self.hora_inicio}, fin={self.hora_fin}")
            raise ValueError("La hora de inicio debe ser anterior a la de fin")

    # -------------------
    # Lógica útil
    # -------------------

    def duracion_horas(self) -> float:
        """Devuelve la duración de la sesión en horas."""
        duracion = (a_minutos(self.hora_fin) - a_minutos(self.hora_inicio)) / 60.0
        log.info(f"Sesion {self.id_sesion or 'sin_id'} ({self.fecha}): duración calculada = {duracion} horas")
        return duracion

    def __repr__(self):
        return f"<Sesion {self.fecha} {self.hora_inicio}-{self.hora_fin}>"

    def to_dict(self):
        data = {
            "id_sesion": self.id_sesion,
            "id_contratacion": self.id_contratacion,
            "fecha": self.fecha,
            "hora_inicio": self.hora_inicio,
            "hora_fin": self.hora_fin,
            "direccion": self.direccion,
            "enlace_vc": self.enlace_vc,
            "estado": self.estado,
            "notas": self.notas,
            "created_at": self.created_at,
        }
        log.debug(f"Sesion.to_dict() llamado: {data}")
        return data
