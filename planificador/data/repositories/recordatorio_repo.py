from planificador.common.registro import get_logger

log = get_logger(__name__)

class RecordatorioRepository:
    """
    Repositorio de acceso a recordatorios.
    Esta versión básica solo sirve para pruebas de UI.
    """
    @staticmethod
    def listar_todos():
        """
        Devuelve una lista de recordatorios simulados.
        En el entorno real consultaría la base de datos.
        """
        log.debug("RecordatorioRepository.listar_todos() llamado (modo dummy).")
        return []
