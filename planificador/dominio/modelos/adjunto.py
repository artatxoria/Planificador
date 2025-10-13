from datetime import datetime
from pathlib import Path
from planificador.common.registro import get_logger

log = get_logger(__name__)

class Adjunto:
    """
    Clase de dominio que representa un adjunto vinculado a clientes, contrataciones o sesiones.
    Incluye validación y registro de actividad.
    """

    def __init__(self, origen, id_origen, ruta_fichero,
                 tipo=None, notas=None, id_adjunto=None, created_at=None):
        self.id_adjunto = id_adjunto
        self.origen = origen  # Ej: "cliente", "contratacion", "sesion"
        self.id_origen = id_origen
        self.tipo = tipo
        self.ruta_fichero = ruta_fichero
        self.notas = notas
        self.created_at = created_at or datetime.now().isoformat()

        self._validar()
        log.info(
            f"Adjunto creado: {self.ruta_fichero} "
            f"(origen={self.origen}, id_origen={self.id_origen}, id={self.id_adjunto or 'pendiente'})"
        )

    def _validar(self):
        if not self.origen:
            log.error("Error al crear Adjunto: falta 'origen'")
            raise ValueError("El adjunto debe tener un origen")
        if not self.id_origen:
            log.error("Error al crear Adjunto: falta 'id_origen'")
            raise ValueError("El adjunto debe estar vinculado a una entidad")
        if not self.ruta_fichero:
            log.error("Error al crear Adjunto: falta 'ruta_fichero'")
            raise ValueError("El adjunto debe tener una ruta de fichero válida")

        # Validación básica de extensión (opcional pero útil para trazabilidad)
        sufijo = Path(self.ruta_fichero).suffix.lower()
        if sufijo not in {".pdf", ".docx", ".odt", ".txt"}:
            log.warning(f"Adjunto {self.ruta_fichero} con extensión poco común: {sufijo}")

    def __repr__(self):
        return f"<Adjunto {self.ruta_fichero} ({self.origen}:{self.id_origen})>"

    def to_dict(self):
        data = {
            "id_adjunto": self.id_adjunto,
            "origen": self.origen,
            "id_origen": self.id_origen,
            "tipo": self.tipo,
            "ruta_fichero": self.ruta_fichero,
            "notas": self.notas,
            "created_at": self.created_at,
        }
        log.debug(f"Adjunto.to_dict() llamado: {data}")
        return data
