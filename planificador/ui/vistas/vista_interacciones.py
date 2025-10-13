from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox
)
from planificador.common.registro import get_logger

log = get_logger(__name__)

try:
    from planificador.data.repositories.interaccion_repo import InteraccionRepository
except Exception:
    InteraccionRepository = None
    log.warning("InteraccionRepository no disponible en vista_interacciones.")


class VistaInteracciones(QWidget):
    """
    Vista para ver y gestionar el historial de interacciones comerciales (mini-CRM).
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        titulo = QLabel("Interacciones (mini-CRM)")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 8px;")
        layout.addWidget(titulo)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Cliente ID", "Fecha", "Tipo", "Resultado", "Descripción"])
        layout.addWidget(self.tabla)

        # Botones
        botones = QHBoxLayout()
        self.btn_recargar = QPushButton("Recargar")
        self.btn_nueva = QPushButton("Nueva interacción")
        botones.addWidget(self.btn_recargar)
        botones.addWidget(self.btn_nueva)
        layout.addLayout(botones)

        self.btn_recargar.clicked.connect(self.cargar_interacciones)

        # carga inicial
        self.cargar_interacciones()

    def cargar_interacciones(self):
        self.tabla.setRowCount(0)
        if InteraccionRepository is None:
            self.tabla.setRowCount(1)
            self.tabla.setItem(0, 0, QTableWidgetItem("Repositorio no disponible"))
            log.debug("InteraccionRepository no disponible en vista_interacciones.")
            return

        try:
            filas = InteraccionRepository.listar_todas()
            self.tabla.setRowCount(len(filas))
            for i, r in enumerate(filas):
                self.tabla.setItem(i, 0, QTableWidgetItem(str(r.get("id_cliente") or "")))
                self.tabla.setItem(i, 1, QTableWidgetItem(str(r.get("fecha") or "")))
                self.tabla.setItem(i, 2, QTableWidgetItem(str(r.get("tipo") or "")))
                self.tabla.setItem(i, 3, QTableWidgetItem(str(r.get("resultado") or "")))
                self.tabla.setItem(i, 4, QTableWidgetItem(str(r.get("descripcion") or "")[:80]))
            self.tabla.resizeColumnsToContents()
            log.info(f"Cargadas {len(filas)} interacciones.")
        except Exception as e:
            log.error(f"Error cargando interacciones: {e}")
            QMessageBox.warning(self, "Error", f"No se pudieron cargar interacciones: {e}")
