from datetime import datetime
from planificador.common.registro import get_logger

log = get_logger(__name__)

class FormacionBase:
    """
    Clase de dominio que representa una formación base (plantilla general).
    Incluye validación y registro de actividad.
    """

    def __init__(self, nombre, id_tema, descripcion=None, horas_referencia=None,
                 nivel=None, contenido_base=None, id_formacion_base=None, created_at=None):
        self.id_formacion_base = id_formacion_base
        self.nombre = nombre
        self.descripcion = descripcion
        self.id_tema = id_tema
        self.horas_referencia = horas_referencia
        self.nivel = nivel
        self.contenido_base = contenido_base
        self.created_at = created_at or datetime.now().isoformat()

        self._validar()
        log.info(f"FormacionBase creada: {self.nombre}, id={self.id_formacion_base or 'pendiente'}, tema={self.id_tema}")

    def _validar(self):
        if not self.nombre:
            log.error("Error al crear FormacionBase: falta 'nombre'")
            raise ValueError("El campo 'nombre' es obligatorio en FormacionBase")
        if not self.id_tema:
            log.error(f"Error al crear FormacionBase {self.nombre or ''}: falta 'id_tema'")
            raise ValueError("Debe asociarse un Tema válido a la formación base")
        if self.horas_referencia is not None and self.horas_referencia <= 0:
            log.error(f"Horas de referencia inválidas en FormacionBase {self.nombre}: {self.horas_referencia}")
            raise ValueError("Las horas de referencia deben ser mayores a 0")

    def __repr__(self):
        return f"<FormacionBase {self.nombre} (Tema {self.id_tema})>"

    def to_dict(self):
        data = {
            "id_formacion_base": self.id_formacion_base,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "id_tema": self.id_tema,
            "horas_referencia": self.horas_referencia,
            "nivel": self.nivel,
            "contenido_base": self.contenido_base,
            "created_at": self.created_at,
        }
        log.debug(f"FormacionBase.to_dict() llamado para {self.nombre}: {data}")
        return data
