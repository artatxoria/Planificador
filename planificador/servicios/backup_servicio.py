import shutil
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Configuración de logging
if not logger.handlers:
    log_path = Path(__file__).resolve().parents[2] / "logs"
    log_path.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_path / "backup.log", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


class ServicioBackup:
    """Servicio para gestionar copias de seguridad locales de la base de datos."""

    @staticmethod
    def realizar_backup(db_path: Path, carpeta_destino: Path, max_copias: int = 5) -> Path:
        """
        Crea una copia de seguridad del archivo de base de datos en la carpeta indicada.
        Mantiene solo las últimas 'max_copias' copias.
        """
        try:
            if not db_path.exists():
                raise FileNotFoundError(f"No se encuentra la base de datos en: {db_path}")

            carpeta_destino.mkdir(parents=True, exist_ok=True)
            fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = carpeta_destino / f"planificador_backup_{fecha}.db"

            shutil.copy2(db_path, backup_path)
            logger.info(f"Backup creado correctamente: {backup_path}")

            # Rotación de copias antiguas
            backups = sorted(carpeta_destino.glob("planificador_backup_*.db"), reverse=True)
            if len(backups) > max_copias:
                for old_backup in backups[max_copias:]:
                    old_backup.unlink()
                    logger.info(f"Backup antiguo eliminado: {old_backup.name}")

            return backup_path

        except Exception as e:
            logger.error(f"Error al crear backup: {e}")
            raise

    @staticmethod
    def listar_backups(carpeta_destino: Path) -> list[Path]:
        """Devuelve una lista ordenada de backups disponibles (más recientes primero)."""
        try:
            backups = sorted(carpeta_destino.glob("planificador_backup_*.db"), reverse=True)
            logger.info(f"{len(backups)} backups encontrados en {carpeta_destino}")
            return backups
        except Exception as e:
            logger.error(f"Error al listar backups: {e}")
            raise

    @staticmethod
    def restaurar_backup(backup_path: Path, db_destino: Path) -> bool:
        """Restaura una copia de seguridad sobre el archivo de base de datos principal."""
        try:
            if not backup_path.exists():
                raise FileNotFoundError(f"No se encuentra el archivo de backup: {backup_path}")
            shutil.copy2(backup_path, db_destino)
            logger.info(f"Base de datos restaurada desde backup: {backup_path.name}")
            return True
        except Exception as e:
            logger.error(f"Error al restaurar backup: {e}")
            return False
