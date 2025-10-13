from datetime import datetime
from planificador.common.registro import get_logger

log = get_logger(__name__)

class Tema:
    """
    Clase de dominio que representa un tema de formación.
    Incluye validación y registro de actividad.
    """

    def __init__(self, nombre, descripcion=None, id_tema=None, created_at=None):
        self.id_tema = id_tema
        self.nombre = nombre
        self.descripcion = descripcion
        self.created_at = created_at or datetime.now().isoformat()

        self._validar()
        log.info(f"Tema creado: {self.nombre}, id={self.id_tema or 'pendiente'}")

    def _validar(self):
        if not self.nombre:
            log.error("Error al crear Tema: falta 'nombre'")
            raise ValueError("El campo 'nombre' es obligatorio para el Tema")

    def __repr__(self):
        return f"<Tema {self.nombre}>"

    def to_dict(self):
        data = {
            "id_tema": self.id_tema,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "created_at": self.created_at,
        }
        log.debug(f"Tema.to_dict() llamado para {self.nombre}: {data}")
        return data
