# planificador/ui/vistas/vista_participantes.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox, QDialog, QFormLayout, QLineEdit,
    QComboBox, QDialogButtonBox
)
from planificador.common.registro import get_logger

log = get_logger(__name__)

try:
    from planificador.data.repositories.participante_repo import ParticipanteRepository
    from planificador.data.repositories.cliente_final_repo import ClienteFinalRepository
except Exception:
    ParticipanteRepository = None
    ClienteFinalRepository = None
    log.warning("Repositorios no disponibles en vista_participantes.")


class DialogoNuevoParticipante(QDialog):
    """
    Diálogo para registrar un nuevo participante en una formación asociada a un cliente final.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Participante")
        self.resize(420, 280)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        # Cliente final asociado
        self.input_cliente_final = QComboBox()
        self._cargar_clientes_finales()
        form.addRow("Cliente Final:", self.input_cliente_final)

        # Datos del participante
        self.input_nombre = QLineEdit()
        form.addRow("Nombre:", self.input_nombre)

        self.input_telefono = QLineEdit()
        form.addRow("Teléfono:", self.input_telefono)

        self.input_email = QLineEdit()
        form.addRow("Email:", self.input_email)

        self.input_notas = QLineEdit()
        form.addRow("Notas:", self.input_notas)

        layout.addLayout(form)

        botones = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        botones.accepted.connect(self._guardar)
        botones.rejected.connect(self.reject)
        layout.addWidget(botones)

    # ----------------------------------------------------------------------
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

    # ----------------------------------------------------------------------
    def _guardar(self):
        """Guarda el participante en la base de datos."""
        if ParticipanteRepository is None:
            QMessageBox.warning(self, "Error", "Repositorio de participantes no disponible.")
            return

        id_cliente_final = self.input_cliente_final.currentData()
        if id_cliente_final in (None, -1):
            QMessageBox.warning(self, "Validación", "Debe seleccionar un cliente final válido.")
            return

        nombre = self.input_nombre.text().strip()
        telefono = self.input_telefono.text().strip()
        email = self.input_email.text().strip()
        notas = self.input_notas.text().strip()

        if not nombre:
            QMessageBox.warning(self, "Validación", "El nombre del participante es obligatorio.")
            return

        try:
            ParticipanteRepository.crear(
                id_cliente_final=id_cliente_final,
                nombre=nombre,
                telefono=telefono or None,
                email=email or None,
                notas=notas or None
            )
            log.info(f"Participante '{nombre}' creado para cliente_final={id_cliente_final}.")
            self.accept()
        except Exception as e:
            log.error(f"Error creando participante: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo crear el participante: {e}")


class VistaParticipantes(QWidget):
    """
    Vista principal para la gestión de participantes de las formaciones.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Participantes de las Formaciones")
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(self.label)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Cliente Final", "Nombre", "Teléfono", "Email", "Notas"])
        layout.addWidget(self.tabla)

        # Botones
        botones = QHBoxLayout()
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_nuevo = QPushButton("Nuevo Participante")
        botones.addWidget(self.btn_actualizar)
        botones.addWidget(self.btn_nuevo)
        layout.addLayout(botones)

        # Conexiones
        self.btn_actualizar.clicked.connect(self.cargar_participantes)
        self.btn_nuevo.clicked.connect(self._abrir_dialogo_nuevo)

        self.cargar_participantes()

    # ----------------------------------------------------------------------
    def _abrir_dialogo_nuevo(self):
        dlg = DialogoNuevoParticipante(self)
        if dlg.exec():
            self.cargar_participantes()

    # ----------------------------------------------------------------------
    def cargar_participantes(self):
        """Carga los participantes desde la base de datos."""
        if ParticipanteRepository is None:
            QMessageBox.warning(self, "Error", "Repositorio de participantes no disponible.")
            return

        try:
            participantes = []
            if ClienteFinalRepository:
                # Obtener los clientes finales y sus participantes
                clientes = ClienteFinalRepository.listar()
                for c in clientes:
                    id_cf = c["id_cliente_final"]
                    lista = ParticipanteRepository.listar_por_cliente_final(id_cf)
                    for p in lista:
                        p["cliente_final_nombre"] = c["empresa"]
                    participantes.extend(lista)

            self.tabla.setRowCount(len(participantes))

            for i, p in enumerate(participantes):
                self.tabla.setItem(i, 0, QTableWidgetItem(p.get("cliente_final_nombre", "")))
                self.tabla.setItem(i, 1, QTableWidgetItem(p.get("nombre", "")))
                self.tabla.setItem(i, 2, QTableWidgetItem(p.get("telefono", "") or ""))
                self.tabla.setItem(i, 3, QTableWidgetItem(p.get("email", "") or ""))
                self.tabla.setItem(i, 4, QTableWidgetItem(p.get("notas", "") or ""))

            self.tabla.resizeColumnsToContents()
            log.info(f"Cargados {len(participantes)} participantes.")
        except Exception as e:
            log.error(f"Error cargando participantes: {e}")
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los participantes: {e}")
