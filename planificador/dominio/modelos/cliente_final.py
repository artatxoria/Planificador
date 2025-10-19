from datetime import datetime
from planificador.common.registro import get_logger

log = get_logger(__name__)

class ClienteFinal:
    """
    Representa la empresa donde se imparte la formación
    cuando la contratación proviene de una agencia intermediaria.
    """

    def __init__(self, empresa, persona_encargada=None, telefono_encargada=None,
                 email_encargada=None, direccion=None, notas=None,
                 id_cliente_final=None, created_at=None):
        self.id_cliente_final = id_cliente_final
        self.empresa = empresa
        self.persona_encargada = persona_encargada
        self.telefono_encargada = telefono_encargada
        self.email_encargada = email_encargada
        self.direccion = direccion
        self.notas = notas
        self.created_at = created_at or datetime.now().isoformat()

        self._validar()
        log.info(f"ClienteFinal creado: empresa={self.empresa}, id={self.id_cliente_final or 'pendiente'}")

    def _validar(self):
        if not self.empresa:
            log.error("Error al crear ClienteFinal: falta 'empresa'")
            raise ValueError("El nombre de la empresa del cliente final es obligatorio")

    def __repr__(self):
        return f"<ClienteFinal {self.empresa}>"

    def to_dict(self):
        data = self.__dict__.copy()
        log.debug(f"ClienteFinal.to_dict() llamado para {self.empresa}: {data}")
        return data
