from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout
)
from planificador.data.repositories.cliente_repo import ClienteRepository


class VistaClientes(QWidget):
    """
    Vista principal para la gestión de clientes.
    Muestra una tabla con los clientes registrados y botones de acción.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Listado de Clientes")
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(self.label)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Empresa", "Persona Contacto", "Email"])
        layout.addWidget(self.tabla)

        # Botones
        botones = QHBoxLayout()
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_nuevo = QPushButton("Nuevo Cliente")
        botones.addWidget(self.btn_actualizar)
        botones.addWidget(self.btn_nuevo)
        layout.addLayout(botones)

        self.btn_actualizar.clicked.connect(self.cargar_clientes)

        self.cargar_clientes()

    def cargar_clientes(self):
        """Carga los clientes desde la base de datos."""
        clientes = ClienteRepository.listar()
        self.tabla.setRowCount(len(clientes))

        for i, c in enumerate(clientes):
            self.tabla.setItem(i, 0, QTableWidgetItem(c["empresa"]))
            self.tabla.setItem(i, 1, QTableWidgetItem(c["persona_contacto"] or ""))
            self.tabla.setItem(i, 2, QTableWidgetItem(c["email"] or ""))

        self.tabla.resizeColumnsToContents()
