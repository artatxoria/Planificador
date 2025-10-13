from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox
)
from planificador.common.registro import get_logger

log = get_logger(__name__)

try:
    from planificador.data.repositories.formacion_base_repo import FormacionBaseRepository
except Exception:
    FormacionBaseRepository = None
    log.warning("FormacionBaseRepository no disponible en vista_formaciones.")


class VistaFormaciones(QWidget):
    """
    Vista para gestionar el catálogo de formaciones (FormacionBase).
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        titulo = QLabel("Formaciones")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 8px;")
        layout.addWidget(titulo)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Nombre", "Tema ID", "Horas ref."])
        layout.addWidget(self.tabla)

        # Botones
        botones = QHBoxLayout()
        self.btn_recargar = QPushButton("Recargar")
        self.btn_nuevo = QPushButton("Nueva formación")
        botones.addWidget(self.btn_recargar)
        botones.addWidget(self.btn_nuevo)
        layout.addLayout(botones)

        self.btn_recargar.clicked.connect(self.cargar_formaciones)

        # carga inicial
        self.cargar_formaciones()

    def cargar_formaciones(self):
        self.tabla.setRowCount(0)
        if FormacionBaseRepository is None:
            self.tabla.setRowCount(1)
            self.tabla.setItem(0, 0, QTableWidgetItem("Repositorio no disponible"))
            log.debug("FormacionBaseRepository no disponible para cargar formaciones.")
            return

        try:
            filas = FormacionBaseRepository.listar()
            self.tabla.setRowCount(len(filas))
            for i, f in enumerate(filas):
                self.tabla.setItem(i, 0, QTableWidgetItem(f["nombre"]))
                self.tabla.setItem(i, 1, QTableWidgetItem(str(f.get("id_tema") or "")))
                self.tabla.setItem(i, 2, QTableWidgetItem(str(f.get("horas_referencia") or "")))
            self.tabla.resizeColumnsToContents()
            log.info(f"Cargadas {len(filas)} formaciones.")
        except Exception as e:
            log.error(f"Error cargando formaciones: {e}")
            QMessageBox.warning(self, "Error", f"No se pudieron cargar formaciones: {e}")
