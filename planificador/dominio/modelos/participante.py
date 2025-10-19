from datetime import datetime
from planificador.common.registro import get_logger

log = get_logger(__name__)

class Participante:
    """
    Representa a un participante individual en una formación impartida en un cliente final.
    """

    def __init__(self, id_cliente_final, nombre, email=None, telefono=None,
                 observaciones=None, id_participante=None, created_at=None):
        self.id_participante = id_participante
        self.id_cliente_final = id_cliente_final
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.observaciones = observaciones
        self.created_at = created_at or datetime.now().isoformat()

        self._validar()
        log.info(f"Participante creado: {self.nombre} (cliente_final={self.id_cliente_final})")

    def _validar(self):
        if not self.id_cliente_final:
            log.error("Error al crear Participante: falta 'id_cliente_final'")
            raise ValueError("El participante debe estar vinculado a un cliente final")
        if not self.nombre:
            log.error("Error al crear Participante: falta 'nombre'")
            raise ValueError("El nombre del participante es obligatorio")

    def __repr__(self):
        return f"<Participante {self.nombre} ClienteFinal {self.id_cliente_final}>"

    def to_dict(self):
        data = self.__dict__.copy()
        log.debug(f"Participante.to_dict() llamado para {self.nombre}: {data}")
        return data
