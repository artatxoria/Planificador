# planificador/ui/vistas/vista_clientes.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox, QDialog, QFormLayout, QLineEdit,
    QDialogButtonBox
)
from planificador.common.registro import get_logger

log = get_logger(__name__)

try:
    from planificador.data.repositories.cliente_repo import ClienteRepository
    from planificador.data.repositories.contratacion_repo import ContratacionRepository
except Exception:
    ClienteRepository = None
    ContratacionRepository = None
    log.warning("Repositorios no disponibles en vista_clientes.")


class DialogoNuevoCliente(QDialog):
    """
    Diálogo para registrar un nuevo cliente.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo cliente")
        self.resize(400, 250)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.input_empresa = QLineEdit()
        form.addRow("Empresa:", self.input_empresa)

        self.input_persona = QLineEdit()
        form.addRow("Persona de contacto:", self.input_persona)

        self.input_email = QLineEdit()
        form.addRow("Email:", self.input_email)

        self.input_telefono = QLineEdit()
        form.addRow("Teléfono:", self.input_telefono)

        layout.addLayout(form)

        botones = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        botones.accepted.connect(self._guardar)
        botones.rejected.connect(self.reject)
        layout.addWidget(botones)

    def _guardar(self):
        if ClienteRepository is None:
            QMessageBox.warning(self, "Error", "Repositorio de clientes no disponible.")
            return

        empresa = self.input_empresa.text().strip()
        persona = self.input_persona.text().strip()
        email = self.input_email.text().strip()
        telefono = self.input_telefono.text().strip()

        if not empresa:
            QMessageBox.warning(self, "Validación", "El nombre de la empresa es obligatorio.")
            return

        try:
            ClienteRepository.crear(empresa=empresa, persona_contacto=persona or None, email=email or None, telefono=telefono or None)
            log.info(f"Cliente '{empresa}' creado correctamente.")
            self.accept()
        except Exception as e:
            log.error(f"Error creando cliente: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo crear el cliente: {e}")


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
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Empresa", "Persona Contacto", "Email", "Propuestas activas"])
        layout.addWidget(self.tabla)

        # Botones
        botones = QHBoxLayout()
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_nuevo = QPushButton("Nuevo Cliente")
        botones.addWidget(self.btn_actualizar)
        botones.addWidget(self.btn_nuevo)
        layout.addLayout(botones)

        self.btn_actualizar.clicked.connect(self.cargar_clientes)
        self.btn_nuevo.clicked.connect(self._abrir_dialogo_nuevo)

        self.cargar_clientes()

    def _abrir_dialogo_nuevo(self):
        dlg = DialogoNuevoCliente(self)
        if dlg.exec():
            self.cargar_clientes()

    def cargar_clientes(self):
        """Carga los clientes desde la base de datos."""
        if ClienteRepository is None:
            QMessageBox.warning(self, "Error", "Repositorio de clientes no disponible.")
            return

        try:
            clientes = ClienteRepository.listar()
            self.tabla.setRowCount(len(clientes))

            for i, c in enumerate(clientes):
                self.tabla.setItem(i, 0, QTableWidgetItem(c.get("empresa", "")))
                self.tabla.setItem(i, 1, QTableWidgetItem(c.get("persona_contacto") or ""))
                self.tabla.setItem(i, 2, QTableWidgetItem(c.get("email") or ""))

                # Contar cuántas contrataciones en estado 'propuesta' tiene este cliente
                propuestas = 0
                if ContratacionRepository:
                    try:
                        contrataciones = ContratacionRepository.listar_por_cliente(c["id_cliente"])
                        propuestas = sum(1 for con in contrataciones if con.get("estado") == "propuesta")
                    except Exception as e:
                        log.warning(f"No se pudieron contar propuestas para cliente {c['id_cliente']}: {e}")

                self.tabla.setItem(i, 3, QTableWidgetItem(str(propuestas)))

            self.tabla.resizeColumnsToContents()
            log.info(f"Cargados {len(clientes)} clientes.")
        except Exception as e:
            log.error(f"Error cargando clientes: {e}")
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los clientes: {e}")
