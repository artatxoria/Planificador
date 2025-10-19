from datetime import datetime
from planificador.data.repositories.sesion_repo import SesionRepository
from planificador.common.utilidades import a_minutos
from planificador.common.registro import get_logger

log = get_logger(__name__)

class Contratacion:
    """
    Clase de dominio que representa la contratación de una formación por parte de un cliente.
    Puede incluir un cliente final (empresa donde se imparte la formación) cuando el contrato
    proviene de una agencia intermediaria.
    """

    def __init__(self, id_cliente, id_formacion_base, expediente,
                 precio_hora=None, horas_previstas=None, modalidad=None,
                 direccion=None, enlace_vc=None,
                 persona_responsable=None, telefono_responsable=None, email_responsable=None,
                 fecha_inicio_prevista=None, fecha_fin_prevista=None,
                 observaciones=None, estado="tentativo", prioridad="media",
                 id_cliente_final=None, cliente_final=None,
                 id_contratacion=None, created_at=None, updated_at=None):
        self.id_contratacion = id_contratacion
        self.id_cliente = id_cliente
        self.id_cliente_final = id_cliente_final        # Nuevo campo (fase 9)
        self.cliente_final = cliente_final              # Campo informativo (no persistente)
        self.id_formacion_base = id_formacion_base
        self.expediente = expediente
        self.precio_hora = precio_hora
        self.horas_previstas = horas_previstas
        self.modalidad = modalidad
        self.direccion = direccion
        self.enlace_vc = enlace_vc
        self.persona_responsable = persona_responsable
        self.telefono_responsable = telefono_responsable
        self.email_responsable = email_responsable
        self.fecha_inicio_prevista = fecha_inicio_prevista
        self.fecha_fin_prevista = fecha_fin_prevista
        self.observaciones = observaciones
        self.estado = estado
        self.prioridad = prioridad
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()

        self._validar()
        log.info(
            f"Contratación creada: expediente={self.expediente}, cliente={self.id_cliente}, "
            f"formacion={self.id_formacion_base}, cliente_final={self.id_cliente_final or 'N/A'}, "
            f"id={self.id_contratacion or 'pendiente'}"
        )

    def _validar(self):
        """Valida la coherencia básica de los datos de contratación."""
        if not self.id_cliente:
            log.error("Error al crear Contratacion: falta 'id_cliente'")
            raise ValueError("La contratación debe estar vinculada a un cliente principal")
        if not self.id_formacion_base:
            log.error("Error al crear Contratacion: falta 'id_formacion_base'")
            raise ValueError("La contratación debe estar vinculada a una formación base")
        if not self.expediente:
            log.error("Error al crear Contratacion: falta 'expediente'")
            raise ValueError("El expediente es obligatorio")
        if self.precio_hora is not None and self.precio_hora <= 0:
            log.error(f"Precio/hora inválido en Contratacion {self.expediente}: {self.precio_hora}")
            raise ValueError("El precio/hora debe ser mayor que 0")

        # Validación ligera para coherencia de cliente_final
        if self.id_cliente_final is not None and not isinstance(self.id_cliente_final, int):
            log.error(f"id_cliente_final inválido ({self.id_cliente_final}) en {self.expediente}")
            raise ValueError("El id_cliente_final debe ser un entero o None")

    # -------------------
    # Lógica de negocio
    # -------------------

    def calcular_horas_totales(self) -> float:
        """Devuelve el total de horas impartidas según las sesiones en BD."""
        if not self.id_contratacion:
            log.warning(f"Contratacion {self.expediente} sin id_contratacion: no se pueden calcular horas.")
            return 0.0
        sesiones = SesionRepository.listar_por_contratacion(self.id_contratacion)
        total = 0.0
        for s in sesiones:
            ini, fin = a_minutos(s["hora_inicio"]), a_minutos(s["hora_fin"])
            total += (fin - ini) / 60.0
        log.info(f"Contratacion {self.expediente}: horas totales calculadas = {total}")
        return total

    def calcular_horas_restantes(self) -> float:
        """Devuelve las horas restantes respecto a las previstas (si hay)."""
        if self.horas_previstas is None:
            log.debug(f"Contratacion {self.expediente}: no hay horas previstas definidas.")
            return 0.0
        restantes = max(self.horas_previstas - self.calcular_horas_totales(), 0.0)
        log.info(f"Contratacion {self.expediente}: horas restantes = {restantes}")
        return restantes

    def calcular_honorarios(self) -> float:
        """Devuelve el total a facturar = horas impartidas * precio_hora."""
        if self.precio_hora is None:
            log.debug(f"Contratacion {self.expediente}: precio_hora no definido.")
            return 0.0
        honorarios = self.calcular_horas_totales() * self.precio_hora
        log.info(f"Contratacion {self.expediente}: honorarios calculados = {honorarios}")
        return honorarios

    def __repr__(self):
        return f"<Contratacion {self.expediente} Cliente {self.id_cliente}" + \
               (f" ClienteFinal {self.id_cliente_final}>" if self.id_cliente_final else ">")

    def to_dict(self):
        data = self.__dict__.copy()
        log.debug(f"Contratacion.to_dict() llamado para {self.expediente}: {data}")
        return data
