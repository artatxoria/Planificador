# planificador/ui/vistas/vista_configuracion.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QFileDialog, QMessageBox, QFrame
)
from pathlib import Path
from planificador.common.registro import get_logger

log = get_logger(__name__)

try:
    from planificador.data.db_manager import DB_PATH, get_connection
except Exception:
    DB_PATH = Path.cwd() / "planificador.db"
    get_connection = None
    log.warning("DB_PATH o get_connection no disponibles; usando configuración por defecto.")


class VistaConfiguracion(QWidget):
    """
    Vista con opciones de configuración y utilidades (backups, exportes, información).
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        titulo = QLabel("Configuración y utilidades")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 8px;")
        layout.addWidget(titulo)

        # Información sobre la base de datos
        self.info_db = QLabel()
        self.info_db.setFrameShape(QFrame.Shape.Box)
        self.info_db.setStyleSheet("background: #f9f9f9; padding: 6px; font-size: 13px;")
        layout.addWidget(self.info_db)

        self._actualizar_info_db()

        # Botones de utilidad
        botones = QHBoxLayout()
        self.btn_backup = QPushButton("Crear backup ahora")
        self.btn_exportar_csv = QPushButton("Exportar Clientes (CSV)")
        self.btn_refrescar_info = QPushButton("Actualizar info DB")
        botones.addWidget(self.btn_backup)
        botones.addWidget(self.btn_exportar_csv)
        botones.addWidget(self.btn_refrescar_info)
        layout.addLayout(botones)

        self.btn_backup.clicked.connect(self._crear_backup)
        self.btn_exportar_csv.clicked.connect(self._exportar_clientes_csv)
        self.btn_refrescar_info.clicked.connect(self._actualizar_info_db)

    # ---------------------------------------------------------
    #   Utilidades principales
    # ---------------------------------------------------------

    def _actualizar_info_db(self):
        """Muestra la ruta de la base de datos y número de tablas."""
        if not DB_PATH.exists():
            self.info_db.setText("❌ No se encontró la base de datos.")
            return

        texto = f"📂 Base de datos: <b>{DB_PATH}</b>"

        if get_connection:
            try:
                with get_connection() as conn:
                    cur = conn.execute(
                        "SELECT count(*) FROM sqlite_master WHERE type='table'"
                    )
                    tablas = cur.fetchone()[0]
                    texto += f"<br>📊 Tablas registradas: {tablas}"
            except Exception as e:
                texto += f"<br>⚠️ No se pudo leer la estructura: {e}"

        self.info_db.setText(texto)
        log.info(f"Información de BD actualizada ({DB_PATH})")

    def _crear_backup(self):
        """Crea un backup de la base de datos en una carpeta elegida."""
        try:
            from planificador.servicios.backup_servicio import ServicioBackup
            carpeta = QFileDialog.getExistingDirectory(self, "Selecciona carpeta de backups")
            if not carpeta:
                return
            carpeta = Path(carpeta)
            backup = ServicioBackup.realizar_backup(DB_PATH, carpeta)
            QMessageBox.information(self, "Backup", f"✅ Backup creado:\n{backup.name}")
            log.info(f"Backup manual creado: {backup}")
        except Exception as e:
            log.error(f"Error al crear backup manual: {e}")
            QMessageBox.warning(self, "Error", f"No se pudo crear backup:\n{e}")

    def _exportar_clientes_csv(self):
        """Exporta la tabla de clientes a CSV."""
        try:
            from planificador.servicios.exportacion_servicio import ServicioExportacion
            ruta, _ = QFileDialog.getSaveFileName(
                self, "Guardar CSV", "clientes.csv", "CSV Files (*.csv)"
            )
            if not ruta:
                return
            ServicioExportacion.exportar_csv("Cliente", Path(ruta))
            QMessageBox.information(self, "Exportar CSV", "✅ Clientes exportados correctamente.")
            log.info(f"Exportación CSV manual de clientes realizada a {ruta}")
        except Exception as e:
            log.error(f"Error exportando clientes a CSV: {e}")
            QMessageBox.warning(self, "Error", f"No se pudo exportar CSV:\n{e}")
