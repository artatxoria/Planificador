from datetime import datetime
from planificador.common.registro import get_logger

log = get_logger(__name__)

class ContactoClienteFinal:
    """
    Representa una persona de contacto asociada al cliente final:
    puede ser la persona encargada de la formación o un participante.
    """

    def __init__(self, id_cliente_final, nombre, telefono=None, email=None,
                 rol="encargado_formacion", notas=None, id_contacto_final=None, created_at=None):
        self.id_contacto_final = id_contacto_final
        self.id_cliente_final = id_cliente_final
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.rol = rol
        self.notas = notas
        self.created_at = created_at or datetime.now().isoformat()

        self._validar()
        log.info(f"ContactoClienteFinal creado: {self.nombre} (rol={self.rol}, cliente_final={self.id_cliente_final})")

    def _validar(self):
        if not self.id_cliente_final:
            log.error("Error al crear ContactoClienteFinal: falta 'id_cliente_final'")
            raise ValueError("El contacto debe estar vinculado a un cliente final")
        if not self.nombre:
            log.error("Error al crear ContactoClienteFinal: falta 'nombre'")
            raise ValueError("El nombre del contacto es obligatorio")
        if self.rol not in ("encargado_formacion", "participante", "otro"):
            log.error(f"Rol inválido en ContactoClienteFinal: {self.rol}")
            raise ValueError("El rol debe ser 'encargado_formacion', 'participante' u 'otro'")

    def __repr__(self):
        return f"<ContactoClienteFinal {self.nombre} ({self.rol})>"

    def to_dict(self):
        data = self.__dict__.copy()
        log.debug(f"ContactoClienteFinal.to_dict() llamado para {self.nombre}: {data}")
        return data
