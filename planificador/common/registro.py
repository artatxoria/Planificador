import logging
import logging.handlers
from pathlib import Path
from typing import Optional
from planificador.common.config import cargar_config

_configurada = False

def _nivel_desde_texto(txt: str) -> int:
    mapa = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    return mapa.get((txt or "INFO").upper(), logging.INFO)

def configurar_registro(archivo: Optional[Path] = None, nivel_texto: Optional[str] = None,
                        max_bytes: Optional[int] = None, copias: Optional[int] = None,
                        forzar: bool = False) -> None:
    """
    Configura el logging de la aplicación.
    - Si no se pasan parámetros, lee de config.json -> registro.
    - Idempotente por defecto; si forzar=True, borra handlers previos y reconfigura.
    """
    global _configurada
    if _configurada and not forzar:
        return

    cfg = cargar_config()
    reg = cfg.get("registro", {})
    ruta = Path(archivo) if archivo else Path(reg.get("archivo", "logs/planificador.log"))
    nivel = _nivel_desde_texto(nivel_texto or reg.get("nivel", "INFO"))
    mbytes = max_bytes if max_bytes is not None else int(reg.get("max_bytes", 1_048_576))
    backups = copias if copias is not None else int(reg.get("copias", 3))

    # Asegura carpeta
    ruta.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()  # raíz

    # 🔑 Elimina handlers previos si forzamos
    if forzar:
        for h in list(logger.handlers):
            logger.removeHandler(h)

    logger.setLevel(nivel)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    # Rotating File
    fhandler = logging.handlers.RotatingFileHandler(
        ruta, maxBytes=mbytes, backupCount=backups, encoding="utf-8"
    )
    fhandler.setFormatter(fmt)
    logger.addHandler(fhandler)

    # Consola
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    _configurada = True


def get_logger(nombre: str) -> logging.Logger:
    """
    Devuelve un logger listo para usar. Configura el sistema si aún no lo está.
    """
    if not _configurada:
        configurar_registro()
    return logging.getLogger(nombre)
