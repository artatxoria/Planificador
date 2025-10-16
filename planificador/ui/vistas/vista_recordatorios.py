from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QMessageBox
)
from planificador.common.registro import get_logger

log = get_logger(__name__)

try:
    from planificador.data.repositories.recordatorio_repo import RecordatorioRepository
except Exception:
    RecordatorioRepository = None
    log.warning("RecordatorioRepository no disponible en vista_recordatorios.")


class VistaRecordatorios(QWidget):
    """
    Vista para listar y generar recordatorios.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # --- Título ---
        titulo = QLabel("Recordatorios")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 8px;")
        layout.addWidget(titulo)

        # --- Tabla ---
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Tipo", "Cliente", "Fecha", "Descripción"])
        layout.addWidget(self.tabla)

        # --- Botones ---
        botones = QHBoxLayout()
        self.btn_recargar = QPushButton("Recargar")
        self.btn_generar = QPushButton("Generar recordatorios")
        botones.addWidget(self.btn_recargar)
        botones.addWidget(self.btn_generar)
        layout.addLayout(botones)

        # Conexiones
        self.btn_recargar.clicked.connect(self.cargar_recordatorios)
        self.btn_generar.clicked.connect(self._generar_recordatorios)

        # Carga inicial
        self.cargar_recordatorios()

    # --------------------------------------------------------------------------------
    # Lógica
    # --------------------------------------------------------------------------------
    def cargar_recordatorios(self):
        """Carga los recordatorios desde el repositorio."""
        self.tabla.setRowCount(0)
        if RecordatorioRepository is None:
            self.tabla.setRowCount(1)
            self.tabla.setItem(0, 0, QTableWidgetItem("Repositorio no disponible"))
            log.debug("RecordatorioRepository no disponible.")
            return

        try:
            filas = RecordatorioRepository.listar_todos()
            if not filas:
                log.info("No hay recordatorios disponibles.")
                # No añadimos ninguna fila: el test espera tabla vacía
                return

            self.tabla.setRowCount(len(filas))
            for i, r in enumerate(filas):
                if isinstance(r, dict):
                    tipo = str(r.get("tipo", ""))
                    cliente = str(r.get("cliente", ""))
                    fecha = str(r.get("fecha", ""))
                    descripcion = str(r.get("descripcion", ""))
                elif isinstance(r, (list, tuple)):
                    tipo, cliente, fecha, descripcion = (str(x) for x in r[:4])
                else:
                    tipo, cliente, fecha, descripcion = str(r), "", "", ""

                self.tabla.setItem(i, 0, QTableWidgetItem(tipo))
                self.tabla.setItem(i, 1, QTableWidgetItem(cliente))
                self.tabla.setItem(i, 2, QTableWidgetItem(fecha))
                self.tabla.setItem(i, 3, QTableWidgetItem(descripcion))

            self.tabla.resizeColumnsToContents()
            log.info(f"Cargados {len(filas)} recordatorios.")
        except Exception as e:
            log.error(f"Error cargando recordatorios: {e}")
            QMessageBox.warning(self, "Error", f"No se pudieron cargar recordatorios: {e}")


    def _generar_recordatorios(self):
        """Simula la generación de nuevos recordatorios (usado por el test)."""
        try:
            from planificador.servicios.servicio_recordatorios import ServicioRecordatorios
            count = ServicioRecordatorios.generar_desde_interacciones()
            QMessageBox.information(self, "Recordatorios", f"Se generaron {count} recordatorios.")
            log.info(f"Generados {count} recordatorios manualmente.")
            self.cargar_recordatorios()
        except Exception as e:
            log.error(f"Error generando recordatorios: {e}")
            QMessageBox.warning(self, "Error", f"No se pudieron generar recordatorios: {e}")
