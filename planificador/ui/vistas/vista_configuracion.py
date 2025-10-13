from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog, QMessageBox
)
from pathlib import Path
from planificador.common.registro import get_logger

log = get_logger(__name__)

try:
    from planificador.data.db_manager import DB_PATH
except Exception:
    DB_PATH = Path.cwd() / "planificador.db"
    log.warning("DB_PATH no encontrado en data.db_manager; usando planificador.db en cwd.")


class VistaConfiguracion(QWidget):
    """
    Vista con opciones de configuración y utilidades (copias, exportes rápidos...).
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        titulo = QLabel("Configuración y utilidades")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 8px;")
        layout.addWidget(titulo)

        # Botones de utilidad
        botones = QHBoxLayout()
        self.btn_backup = QPushButton("Crear backup ahora")
        self.btn_exportar_csv = QPushButton("Exportar Clientes (CSV)")
        botones.addWidget(self.btn_backup)
        botones.addWidget(self.btn_exportar_csv)
        layout.addLayout(botones)

        self.btn_backup.clicked.connect(self._crear_backup)
        self.btn_exportar_csv.clicked.connect(self._exportar_clientes_csv)

    def _crear_backup(self):
        try:
            from planificador.servicios.backup_servicio import ServicioBackup
            carpeta = QFileDialog.getExistingDirectory(self, "Selecciona carpeta de backups")
            if not carpeta:
                return
            carpeta = Path(carpeta)
            backup = ServicioBackup.realizar_backup(DB_PATH, carpeta)
            QMessageBox.information(self, "Backup", f"Backup creado: {backup.name}")
            log.info(f"Backup manual creado: {backup}")
        except Exception as e:
            log.error(f"Error al crear backup manual: {e}")
            QMessageBox.warning(self, "Error", f"No se pudo crear backup: {e}")

    def _exportar_clientes_csv(self):
        try:
            from planificador.servicios.exportacion_servicio import ServicioExportacion
            ruta, _ = QFileDialog.getSaveFileName(self, "Guardar CSV", "clientes.csv", "CSV Files (*.csv)")
            if not ruta:
                return
            ServicioExportacion.exportar_csv("Cliente", Path(ruta))
            QMessageBox.information(self, "Exportar CSV", "Clientes exportados correctamente.")
            log.info(f"Exportación CSV manual de clientes realizada a {ruta}")
        except Exception as e:
            log.error(f"Error exportando clientes a CSV: {e}")
            QMessageBox.warning(self, "Error", f"No se pudo exportar CSV: {e}")
