import csv
import logging
from pathlib import Path
from datetime import datetime

from planificador.data.db_manager import get_connection

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Configuración de log
if not logger.handlers:
    log_path = Path(__file__).resolve().parents[2] / "logs"
    log_path.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_path / "exportacion.log", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


class ServicioExportacion:
    """Servicio para exportar datos del planificador en distintos formatos."""

    @staticmethod
    def exportar_csv(nombre_tabla: str, ruta_destino: Path) -> Path:
        """Exporta una tabla completa a CSV."""
        try:
            logger.info(f"Exportando tabla {nombre_tabla} a CSV...")

            with get_connection() as conn:
                cursor = conn.execute(f"SELECT * FROM {nombre_tabla}")
                columnas = [desc[0] for desc in cursor.description]
                registros = cursor.fetchall()

            ruta_destino.parent.mkdir(parents=True, exist_ok=True)

            with open(ruta_destino, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(columnas)
                writer.writerows([tuple(r) for r in registros])

            logger.info(f"Exportación CSV completada: {ruta_destino}")
            return ruta_destino

        except Exception as e:
            logger.error(f"Error al exportar {nombre_tabla} a CSV: {e}")
            raise

    @staticmethod
    def exportar_ical(sesiones: list[dict], ruta_destino: Path) -> Path:
        """Exporta una lista de sesiones a formato iCal (.ics)."""
        try:
            logger.info(f"Generando archivo iCal con {len(sesiones)} sesiones...")

            ruta_destino.parent.mkdir(parents=True, exist_ok=True)
            with open(ruta_destino, "w", encoding="utf-8") as f:
                f.write("BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Planificador//ES\n")

                for s in sesiones:
                    f.write("BEGIN:VEVENT\n")
                    f.write(f"SUMMARY:{s.get('titulo', 'Sesión de formación')}\n")
                    f.write(f"DTSTART:{s['fecha']}T{s['hora_inicio'].replace(':', '')}00\n")
                    f.write(f"DTEND:{s['fecha']}T{s['hora_fin'].replace(':', '')}00\n")
                    if s.get("descripcion"):
                        f.write(f"DESCRIPTION:{s['descripcion']}\n")
                    f.write("END:VEVENT\n")

                f.write("END:VCALENDAR\n")

            logger.info(f"Archivo iCal generado: {ruta_destino}")
            return ruta_destino

        except Exception as e:
            logger.error(f"Error al generar iCal: {e}")
            raise

    @staticmethod
    def exportar_pdf(datos: str, vista: str, ruta_destino: Path) -> Path:
        """Exporta un texto simple a PDF (estructura base, sin maquetación)."""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas

            logger.info(f"Generando PDF de vista '{vista}'...")

            ruta_destino.parent.mkdir(parents=True, exist_ok=True)
            c = canvas.Canvas(str(ruta_destino), pagesize=A4)
            c.setFont("Helvetica", 12)
            c.drawString(50, 800, f"Vista: {vista}")
            c.drawString(50, 780, f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            c.drawString(50, 760, "-" * 70)

            y = 740
            for linea in datos.splitlines():
                c.drawString(50, y, linea)
                y -= 15
                if y < 50:
                    c.showPage()
                    y = 800

            c.save()
            logger.info(f"Archivo PDF generado: {ruta_destino}")
            return ruta_destino

        except ImportError:
            msg = "reportlab no está instalado. Instálalo con: pip install reportlab"
            logger.error(msg)
            raise RuntimeError(msg)
        except Exception as e:
            logger.error(f"Error al generar PDF: {e}")
            raise
