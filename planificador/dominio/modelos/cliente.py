from datetime import datetime
from planificador.common.registro import get_logger

log = get_logger(__name__)

class Cliente:
    """
    Clase de dominio que representa un cliente.
    Incluye lógica de validación y registro de actividad.
    """

    def __init__(self, empresa, cif, persona_contacto=None, telefono=None,
                 email=None, direccion=None, notas=None, color_hex="#377eb8",
                 id_cliente=None, created_at=None):
        self.id_cliente = id_cliente
        self.empresa = empresa
        self.persona_contacto = persona_contacto
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.cif = cif
        self.notas = notas
        self.color_hex = color_hex
        self.created_at = created_at or datetime.now().isoformat()

        self._validar()
        log.info(f"Cliente creado: {self.empresa} ({self.cif}), id={self.id_cliente or 'pendiente'}")

    def _validar(self):
        if not self.empresa:
            log.error("Error al crear Cliente: falta 'empresa'")
            raise ValueError("El campo 'empresa' es obligatorio")
        if not self.cif:
            log.error("Error al crear Cliente: falta 'cif'")
            raise ValueError("El campo 'cif' es obligatorio")
        if self.email and "@" not in self.email:
            log.error(f"Email inválido para Cliente {self.empresa}: {self.email}")
            raise ValueError("El campo 'email' no es válido")
        if self.color_hex and not self.color_hex.startswith("#"):
            log.error(f"Código de color inválido para Cliente {self.empresa}: {self.color_hex}")
            raise ValueError("El campo 'color_hex' debe ser un código hexadecimal")

    def __repr__(self):
        return f"<Cliente {self.empresa} ({self.cif})>"

    def resumen_contacto(self):
        resumen = f"{self.persona_contacto or 'Sin contacto'} - {self.telefono or 'Sin teléfono'} - {self.email or 'Sin email'}"
        log.debug(f"Resumen contacto para Cliente {self.empresa}: {resumen}")
        return resumen

    def to_dict(self):
        data = {
            "id_cliente": self.id_cliente,
            "empresa": self.empresa,
            "persona_contacto": self.persona_contacto,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion,
            "cif": self.cif,
            "notas": self.notas,
            "color_hex": self.color_hex,
            "created_at": self.created_at,
        }
        log.debug(f"Cliente.to_dict() llamado para {self.empresa}: {data}")
        return data
