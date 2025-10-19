# planificador/ui/vistas/vista_contactos_clientes_finales.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox, QDialog, QFormLayout, QLineEdit,
    QComboBox, QDialogButtonBox
)
from planificador.common.registro import get_logger

log = get_logger(__name__)

try:
    from planificador.data.repositories.contacto_cliente_final_repo import ContactoClienteFinalRepository
    from planificador.data.repositories.cliente_final_repo import ClienteFinalRepository
except Exception:
    ContactoClienteFinalRepository = None
    ClienteFinalRepository = None
    log.warning("Repositorios no disponibles en vista_contactos_clientes_finales.")


class DialogoNuevoContacto(QDialog):
    """
    Diálogo para registrar un nuevo contacto asociado a un cliente final.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Contacto de Cliente Final")
        self.resize(420, 300)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        # Cliente final asociado
        self.input_cliente_final = QComboBox()
        self._cargar_clientes_finales()
        form.addRow("Cliente Final:", self.input_cliente_final)

        # Campos del contacto
        self.input_nombre = QLineEdit()
        form.addRow("Nombre:", self.input_nombre)

        self.input_telefono = QLineEdit()
        form.addRow("Teléfono:", self.input_telefono)

        self.input_email = QLineEdit()
        form.addRow("Email:", self.input_email)

        self.input_rol = QComboBox()
        self.input_rol.addItems(["encargado_formacion", "participante", "otro"])
        form.addRow("Rol:", self.input_rol)

        self.input_notas = QLineEdit()
        form.addRow("Notas:", self.input_notas)

        layout.addLayout(form)

        botones = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        botones.accepted.connect(self._guardar)
        botones.rejected.connect(self.reject)
        layout.addWidget(botones)

    def _cargar_clientes_finales(self):
        """Carga los clientes finales en el desplegable."""
        if ClienteFinalRepository is None:
            return

        try:
            clientes = ClienteFinalRepository.listar()
            for c in clientes:
                nombre = c.get("empresa", "")
                self.input_cliente_final.addItem(nombre, c["id_cliente_final"])
            if not clientes:
                self.input_cliente_final.addItem("⚠️ No hay clientes finales registrados", -1)
        except Exception as e:
            log.error(f"Error cargando clientes finales en diálogo: {e}")
            self.input_cliente_final.addItem("⚠️ Error al cargar", -1)

    def _guardar(self):
        if ContactoClienteFinalRepository is None:
            QMessageBox.warning(self, "Error", "Repositorio de contactos no disponible.")
            return

        id_cliente_final = self.input_cliente_final.currentData()
        if id_cliente_final in (None, -1):
            QMessageBox.warning(self, "Validación", "Debe seleccionar un cliente final válido.")
            return

        nombre = self.input_nombre.text().strip()
        telefono = self.input_telefono.text().strip()
        email = self.input_email.text().strip()
        rol = self.input_rol.currentText()
        notas = self.input_notas.text().strip()

        if not nombre:
            QMessageBox.warning(self, "Validación", "El nombre del contacto es obligatorio.")
            return

        try:
            ContactoClienteFinalRepository.crear(
                id_cliente_final=id_cliente_final,
                nombre=nombre,
                telefono=telefono or None,
                email=email or None,
                rol=rol,
                notas=notas or None
            )
            log.info(f"Contacto '{nombre}' creado para cliente_final={id_cliente_final}.")
            self.accept()
        except Exception as e:
            log.error(f"Error creando contacto: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo crear el contacto: {e}")


class VistaContactosClientesFinales(QWidget):
    """
    Vista principal para la gestión de contactos asociados a los clientes finales.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Contactos de Clientes Finales")
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(self.label)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Cliente Final", "Nombre", "Rol", "Teléfono", "Email"])
        layout.addWidget(self.tabla)

        # Botones
        botones = QHBoxLayout()
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_nuevo = QPushButton("Nuevo Contacto")
        botones.addWidget(self.btn_actualizar)
        botones.addWidget(self.btn_nuevo)
        layout.addLayout(botones)

        # Conexiones
        self.btn_actualizar.clicked.connect(self.cargar_contactos)
        self.btn_nuevo.clicked.connect(self._abrir_dialogo_nuevo)

        self.cargar_contactos()

    # ------------------------------------------------------------------
    # Métodos internos
    # ------------------------------------------------------------------
    def _abrir_dialogo_nuevo(self):
        dlg = DialogoNuevoContacto(self)
        if dlg.exec():
            self.cargar_contactos()

    def cargar_contactos(self):
        """Carga todos los contactos desde la base de datos."""
        if ContactoClienteFinalRepository is None:
            QMessageBox.warning(self, "Error", "Repositorio de contactos no disponible.")
            return

        try:
            contactos = []
            if ClienteFinalRepository:
                # Recorrer todos los clientes finales y obtener sus contactos
                clientes = ClienteFinalRepository.listar()
                for c in clientes:
                    id_cf = c["id_cliente_final"]
                    lista = ContactoClienteFinalRepository.listar_por_cliente_final(id_cf)
                    for contacto in lista:
                        contacto["cliente_final_nombre"] = c["empresa"]
                    contactos.extend(lista)

            self.tabla.setRowCount(len(contactos))

            for i, c in enumerate(contactos):
                self.tabla.setItem(i, 0, QTableWidgetItem(c.get("cliente_final_nombre", "")))
                self.tabla.setItem(i, 1, QTableWidgetItem(c.get("nombre", "")))
                self.tabla.setItem(i, 2, QTableWidgetItem(c.get("rol", "")))
                self.tabla.setItem(i, 3, QTableWidgetItem(c.get("telefono", "") or ""))
                self.tabla.setItem(i, 4, QTableWidgetItem(c.get("email", "") or ""))

            self.tabla.resizeColumnsToContents()
            log.info(f"Cargados {len(contactos)} contactos de clientes finales.")
        except Exception as e:
            log.error(f"Error cargando contactos: {e}")
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los contactos: {e}")
