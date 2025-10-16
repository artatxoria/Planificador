# planificador/ui/vistas/vista_interacciones.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox, QDialog, QFormLayout, QLineEdit,
    QDateEdit, QComboBox, QTextEdit, QDialogButtonBox, QCheckBox
)
from PyQt6.QtCore import QDate
from datetime import datetime
from planificador.common.registro import get_logger

log = get_logger(__name__)

try:
    from planificador.data.repositories.interaccion_repo import InteraccionRepository
    from planificador.data.repositories.sesion_repo import SesionRepository
    from planificador.data.repositories.contratacion_repo import ContratacionRepository
except Exception:
    InteraccionRepository = None
    SesionRepository = None
    ContratacionRepository = None
    log.warning("Repositorios no disponibles en vista_interacciones.")


class DialogoNuevaInteraccion(QDialog):
    """
    Diálogo para registrar una nueva interacción comercial.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nueva interacción comercial")
        self.resize(400, 350)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.input_id_cliente = QLineEdit()
        form.addRow("ID Cliente:", self.input_id_cliente)

        self.input_fecha = QDateEdit()
        self.input_fecha.setCalendarPopup(True)
        self.input_fecha.setDate(QDate.currentDate())
        form.addRow("Fecha:", self.input_fecha)

        self.input_tipo = QComboBox()
        self.input_tipo.addItems(["llamada", "reunión", "email", "visita", "otros"])
        form.addRow("Tipo:", self.input_tipo)

        self.input_resultado = QLineEdit()
        form.addRow("Resultado:", self.input_resultado)

        self.input_descripcion = QTextEdit()
        form.addRow("Descripción:", self.input_descripcion)

        self.input_proxima_accion = QLineEdit()
        form.addRow("Próxima acción:", self.input_proxima_accion)

        self.chk_crear_propuesta = QCheckBox("Crear sesión en estado 'propuesta'")
        form.addRow("", self.chk_crear_propuesta)

        layout.addLayout(form)

        # Botones
        botones = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        botones.accepted.connect(self._guardar)
        botones.rejected.connect(self.reject)
        layout.addWidget(botones)

    def _guardar(self):
        if InteraccionRepository is None:
            QMessageBox.warning(self, "Error", "Repositorio de interacciones no disponible.")
            return

        try:
            id_cliente = int(self.input_id_cliente.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Validación", "Debe indicar un ID de cliente numérico.")
            return

        fecha = self.input_fecha.date().toString("yyyy-MM-dd")
        tipo = self.input_tipo.currentText()
        resultado = self.input_resultado.text().strip()
        descripcion = self.input_descripcion.toPlainText().strip()
        proxima_accion = self.input_proxima_accion.text().strip()

        try:
            # Registrar interacción
            InteraccionRepository.crear(
                id_cliente=id_cliente,
                fecha=fecha,
                tipo=tipo,
                descripcion=descripcion,
                resultado=resultado or None,
                proxima_accion=proxima_accion or None
            )
            log.info(f"Interacción creada para cliente {id_cliente} ({tipo})")

            # Si se marca la casilla, crear sesión en estado 'propuesta'
            if self.chk_crear_propuesta.isChecked() and SesionRepository and ContratacionRepository:
                try:
                    contrataciones = ContratacionRepository.listar_por_cliente(id_cliente)
                    if contrataciones:
                        id_contratacion = contrataciones[0]["id_contratacion"]
                        SesionRepository.crear(
                            id_contratacion=id_contratacion,
                            fecha=datetime.now().strftime("%Y-%m-%d"),
                            hora_inicio="09:00",
                            hora_fin="10:00",
                            direccion=None,
                            estado="propuesta",
                            notas="Generada automáticamente desde interacción comercial"
                        )
                        log.info(f"Sesión en estado 'propuesta' creada para cliente {id_cliente}")
                    else:
                        log.warning(f"No se encontró contratación para cliente {id_cliente}, no se creó sesión propuesta.")
                except Exception as e:
                    log.error(f"Error creando sesión propuesta: {e}")

            self.accept()

        except Exception as e:
            log.error(f"Error creando interacción: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo crear la interacción: {e}")


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
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels([
            "Cliente ID", "Fecha", "Tipo", "Resultado", "Descripción", "Próxima acción"
        ])
        layout.addWidget(self.tabla)

        # Botones
        botones = QHBoxLayout()
        self.btn_recargar = QPushButton("Recargar")
        self.btn_nueva = QPushButton("Nueva interacción")
        botones.addWidget(self.btn_recargar)
        botones.addWidget(self.btn_nueva)
        layout.addLayout(botones)

        self.btn_recargar.clicked.connect(self.cargar_interacciones)
        self.btn_nueva.clicked.connect(self._abrir_dialogo_nueva)

        # carga inicial
        self.cargar_interacciones()

    def _abrir_dialogo_nueva(self):
        dlg = DialogoNuevaInteraccion(self)
        if dlg.exec():
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
                self.tabla.setItem(i, 5, QTableWidgetItem(str(r.get("proxima_accion") or "")))
            self.tabla.resizeColumnsToContents()
            log.info(f"Cargadas {len(filas)} interacciones.")
        except Exception as e:
            log.error(f"Error cargando interacciones: {e}")
            QMessageBox.warning(self, "Error", f"No se pudieron cargar interacciones: {e}")
