# planificador/ui/vistas/vista_clientes_finales.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox, QDialog, QFormLayout, QLineEdit,
    QDialogButtonBox
)
from planificador.common.registro import get_logger

log = get_logger(__name__)

try:
    from planificador.data.repositories.cliente_final_repo import ClienteFinalRepository
except Exception:
    ClienteFinalRepository = None
    log.warning("Repositorio ClienteFinalRepository no disponible en vista_clientes_finales.")


class DialogoNuevoClienteFinal(QDialog):
    """
    Diálogo para registrar un nuevo cliente final (empresa donde se imparte la formación).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Cliente Final")
        self.resize(420, 320)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.input_empresa = QLineEdit()
        form.addRow("Empresa:", self.input_empresa)

        self.input_encargado = QLineEdit()
        form.addRow("Persona encargada:", self.input_encargado)

        self.input_email = QLineEdit()
        form.addRow("Email encargada:", self.input_email)

        self.input_telefono = QLineEdit()
        form.addRow("Teléfono encargada:", self.input_telefono)

        self.input_direccion = QLineEdit()
        form.addRow("Dirección:", self.input_direccion)

        self.input_notas = QLineEdit()
        form.addRow("Notas:", self.input_notas)

        layout.addLayout(form)

        botones = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        botones.accepted.connect(self._guardar)
        botones.rejected.connect(self.reject)
        layout.addWidget(botones)

    def _guardar(self):
        if ClienteFinalRepository is None:
            QMessageBox.warning(self, "Error", "Repositorio de clientes finales no disponible.")
            return

        empresa = self.input_empresa.text().strip()
        encargado = self.input_encargado.text().strip()
        email = self.input_email.text().strip()
        telefono = self.input_telefono.text().strip()
        direccion = self.input_direccion.text().strip()
        notas = self.input_notas.text().strip()

        if not empresa:
            QMessageBox.warning(self, "Validación", "El nombre de la empresa es obligatorio.")
            return

        try:
            ClienteFinalRepository.crear(
                empresa=empresa,
                persona_encargada=encargado or None,
                email_encargada=email or None,
                telefono_encargada=telefono or None,
                direccion=direccion or None,
                notas=notas or None
            )
            log.info(f"Cliente Final '{empresa}' creado correctamente.")
            self.accept()
        except Exception as e:
            log.error(f"Error creando cliente final: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo crear el cliente final: {e}")


class VistaClientesFinales(QWidget):
    """
    Vista principal para la gestión de clientes finales.
    Muestra una tabla con los clientes finales registrados y botones de acción.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Listado de Clientes Finales")
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(self.label)

        # Tabla principal
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Empresa", "Encargada", "Email", "Teléfono", "Dirección"])
        layout.addWidget(self.tabla)

        # Botones de acción
        botones = QHBoxLayout()
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_nuevo = QPushButton("Nuevo Cliente Final")
        botones.addWidget(self.btn_actualizar)
        botones.addWidget(self.btn_nuevo)
        layout.addLayout(botones)

        # Conexiones
        self.btn_actualizar.clicked.connect(self.cargar_clientes_finales)
        self.btn_nuevo.clicked.connect(self._abrir_dialogo_nuevo)

        # Cargar datos iniciales
        self.cargar_clientes_finales()

    # ------------------------------------------------------------------
    # Métodos internos
    # ------------------------------------------------------------------
    def _abrir_dialogo_nuevo(self):
        dlg = DialogoNuevoClienteFinal(self)
        if dlg.exec():
            self.cargar_clientes_finales()

    def cargar_clientes_finales(self):
        """Carga los clientes finales desde la base de datos."""
        if ClienteFinalRepository is None:
            QMessageBox.warning(self, "Error", "Repositorio de clientes finales no disponible.")
            return

        try:
            clientes = ClienteFinalRepository.listar()
            self.tabla.setRowCount(len(clientes))

            for i, c in enumerate(clientes):
                self.tabla.setItem(i, 0, QTableWidgetItem(c.get("empresa", "")))
                self.tabla.setItem(i, 1, QTableWidgetItem(c.get("persona_encargada") or ""))
                self.tabla.setItem(i, 2, QTableWidgetItem(c.get("email_encargada") or ""))
                self.tabla.setItem(i, 3, QTableWidgetItem(c.get("telefono_encargada") or ""))
                self.tabla.setItem(i, 4, QTableWidgetItem(c.get("direccion") or ""))

            self.tabla.resizeColumnsToContents()
            log.info(f"Cargados {len(clientes)} clientes finales.")
        except Exception as e:
            log.error(f"Error cargando clientes finales: {e}")
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los clientes finales: {e}")
