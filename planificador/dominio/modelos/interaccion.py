from datetime import datetime
from planificador.common.registro import get_logger

log = get_logger(__name__)

class InteraccionCliente:
    """
    Clase de dominio que representa una interacción comercial con un cliente.
    Incluye validación, control de estado y registro de actividad.
    """

    RESULTADOS_VALIDOS = {"pendiente", "negociacion", "aceptado", "rechazado", "sin_respuesta"}
    TIPOS_VALIDOS = {"llamada", "email", "reunion", "mensaje", "otro"}

    def __init__(self, id_cliente, fecha, tipo, descripcion=None,
                 resultado="pendiente", proxima_accion=None, fecha_proxima_accion=None,
                 crear_recordatorio=False, id_contratacion=None,
                 id_interaccion=None, created_at=None):
        self.id_interaccion = id_interaccion
        self.id_cliente = id_cliente
        self.id_contratacion = id_contratacion
        self.fecha = fecha
        self.tipo = tipo
        self.descripcion = descripcion
        self.resultado = resultado
        self.proxima_accion = proxima_accion
        self.fecha_proxima_accion = fecha_proxima_accion
        self.crear_recordatorio = bool(crear_recordatorio)
        self.created_at = created_at or datetime.now().isoformat()

        self._validar()
        log.info(f"Interaccion creada: cliente={self.id_cliente}, tipo={self.tipo}, resultado={self.resultado}, id={self.id_interaccion or 'pendiente'}")

    def _validar(self):
        if not self.id_cliente:
            log.error("Error al crear InteraccionCliente: falta 'id_cliente'")
            raise ValueError("La interacción debe estar vinculada a un cliente")
        if not self.fecha:
            log.error("Error al crear InteraccionCliente: falta 'fecha'")
            raise ValueError("La interacción debe tener una fecha")
        if self.tipo not in self.TIPOS_VALIDOS:
            log.error(f"Tipo inválido en InteraccionCliente: {self.tipo}")
            raise ValueError(f"El tipo de interacción debe ser uno de {self.TIPOS_VALIDOS}")
        if self.resultado not in self.RESULTADOS_VALIDOS:
            log.error(f"Resultado inválido en InteraccionCliente: {self.resultado}")
            raise ValueError(f"El resultado debe ser uno de {self.RESULTADOS_VALIDOS}")

    # -------------------
    # Lógica útil
    # -------------------

    def requiere_recordatorio(self) -> bool:
        """Indica si debe crearse un recordatorio para esta interacción."""
        necesita = self.crear_recordatorio and self.proxima_accion and self.fecha_proxima_accion
        log.info(f"Interaccion {self.id_interaccion or 'sin_id'} (cliente={self.id_cliente}): requiere_recordatorio={necesita}")
        return necesita

    def __repr__(self):
        return f"<InteraccionCliente {self.tipo} {self.fecha} ({self.resultado})>"

    def to_dict(self):
        data = {
            "id_interaccion": self.id_interaccion,
            "id_cliente": self.id_cliente,
            "id_contratacion": self.id_contratacion,
            "fecha": self.fecha,
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "resultado": self.resultado,
            "proxima_accion": self.proxima_accion,
            "fecha_proxima_accion": self.fecha_proxima_accion,
            "crear_recordatorio": self.crear_recordatorio,
            "created_at": self.created_at,
        }
        log.debug(f"InteraccionCliente.to_dict() llamado: {data}")
        return data
