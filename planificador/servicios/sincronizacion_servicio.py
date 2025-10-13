import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Configuración del log
if not logger.handlers:
    log_path = Path(__file__).resolve().parents[2] / "logs"
    log_path.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_path / "sincronizacion.log", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


class ServicioSincronizacion:
    """Simula la sincronización con Google Calendar."""

    @staticmethod
    def exportar_a_google_calendar(sesiones: list[dict]) -> int:
        """
        Simula la exportación de sesiones a Google Calendar.
        Devuelve el número de sesiones "exportadas".
        """
        logger.info(f"Simulando exportación de {len(sesiones)} sesiones a Google Calendar...")
        exportadas = 0

        try:
            for s in sesiones:
                logger.info(
                    f"Exportada sesión simulada: {s.get('titulo', 'Sesión')} "
                    f"({s['fecha']} {s['hora_inicio']}-{s['hora_fin']})"
                )
                exportadas += 1

            logger.info(f"Exportación simulada completada ({exportadas} sesiones).")
            return exportadas

        except Exception as e:
            logger.error(f"Error durante la exportación simulada: {e}")
            raise

    @staticmethod
    def importar_desde_google_calendar() -> list[dict]:
        """
        Simula la importación de eventos desde Google Calendar.
        Devuelve una lista de eventos simulados.
        """
        logger.info("Simulando importación de eventos desde Google Calendar...")

        try:
            eventos = [
                {
                    "titulo": "Reunión con cliente Demo",
                    "fecha": "2025-10-10",
                    "hora_inicio": "10:00",
                    "hora_fin": "11:00",
                    "descripcion": "Evento simulado importado de Google Calendar"
                },
                {
                    "titulo": "Curso de Excel - Empresa A",
                    "fecha": "2025-10-12",
                    "hora_inicio": "09:00",
                    "hora_fin": "13:00",
                    "descripcion": "Simulación de importación"
                }
            ]

            logger.info(f"Importación simulada completada ({len(eventos)} eventos).")
            return eventos

        except Exception as e:
            logger.error(f"Error durante la importación simulada: {e}")
            raise

    @staticmethod
    def verificar_credenciales() -> bool:
        """
        Simula la verificación de credenciales de Google Calendar.
        """
        logger.info("Verificando credenciales simuladas de Google Calendar...")
        try:
            # En una versión real aquí se verificaría el token OAuth2
            return True
        except Exception as e:
            logger.error(f"Error al verificar credenciales: {e}")
            return False
