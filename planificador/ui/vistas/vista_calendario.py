# planificador/ui/vistas/vista_calendario.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCalendarWidget, QListWidget, QPushButton,
    QHBoxLayout, QMessageBox, QDialog, QFormLayout, QLineEdit, QTimeEdit,
    QDialogButtonBox, QComboBox
)
from PyQt6.QtCore import QDate, QTime
from datetime import datetime
from planificador.common.registro import get_logger

log = get_logger(__name__)

try:
    from planificador.data.repositories.sesion_repo import SesionRepository
    from planificador.data.repositories.contratacion_repo import ContratacionRepository
except Exception:
    SesionRepository = None
    ContratacionRepository = None
    log.warning("SesionRepository o ContratacionRepository no disponible en vista_calendario.")


class DialogoNuevaSesion(QDialog):
    """
    Diálogo modal para crear una nueva sesión (incluyendo 'propuesta').
    """

    def __init__(self, parent=None, fecha_preseleccionada=None):
        super().__init__(parent)
        self.setWindowTitle("Nueva sesión")
        self.resize(350, 250)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        # Fecha sugerida
        self.input_fecha = QLineEdit()
        if fecha_preseleccionada:
            self.input_fecha.setText(fecha_preseleccionada)
        form.addRow("Fecha (AAAA-MM-DD):", self.input_fecha)

        self.input_hora_inicio = QTimeEdit()
        self.input_hora_inicio.setDisplayFormat("HH:mm")
        self.input_hora_inicio.setTime(QTime.currentTime())
        form.addRow("Hora inicio:", self.input_hora_inicio)

        self.input_hora_fin = QTimeEdit()
        self.input_hora_fin.setDisplayFormat("HH:mm")
        self.input_hora_fin.setTime(QTime.currentTime().addSecs(3600))
        form.addRow("Hora fin:", self.input_hora_fin)

        # Contratación (combo simple)
        self.combo_contratacion = QComboBox()
        form.addRow("Contratación:", self.combo_contratacion)

        # Estado de la sesión (nuevo)
        self.combo_estado = QComboBox()
        self.combo_estado.addItems(["propuesta", "programada", "reprogramada", "cancelada"])
        form.addRow("Estado:", self.combo_estado)

        self.input_direccion = QLineEdit()
        form.addRow("Dirección:", self.input_direccion)

        layout.addLayout(form)

        # Botones
        botones = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        botones.accepted.connect(self._guardar)
        botones.rejected.connect(self.reject)
        layout.addWidget(botones)

        # Cargar contrataciones disponibles
        self._cargar_contrataciones()

    def _cargar_contrataciones(self):
        if ContratacionRepository is None:
            self.combo_contratacion.addItem("Sin repositorio de contrataciones")
            self.combo_contratacion.setEnabled(False)
            return
        try:
            filas = ContratacionRepository.listar_todas()
            if not filas:
                self.combo_contratacion.addItem("No hay contrataciones")
                self.combo_contratacion.setEnabled(False)
                return
            for f in filas:
                etiqueta = f"{f['id_contratacion']} - {f.get('expediente', '')}"
                self.combo_contratacion.addItem(etiqueta, f["id_contratacion"])
        except Exception as e:
            log.error(f"Error cargando contrataciones: {e}")
            self.combo_contratacion.addItem("Error cargando contrataciones")
            self.combo_contratacion.setEnabled(False)

    def _guardar(self):
        if SesionRepository is None:
            QMessageBox.warning(self, "Error", "Repositorio de sesiones no disponible.")
            return

        fecha = self.input_fecha.text().strip()
        hora_inicio = self.input_hora_inicio.time().toString("HH:mm")
        hora_fin = self.input_hora_fin.time().toString("HH:mm")
        direccion = self.input_direccion.text().strip() or None
        estado = self.combo_estado.currentText()

        id_contratacion = self.combo_contratacion.currentData()
        if not id_contratacion:
            QMessageBox.warning(self, "Validación", "Debe seleccionar una contratación válida.")
            return

        try:
            SesionRepository.crear(
                id_contratacion=id_contratacion,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                direccion=direccion,
                estado=estado
            )
            log.info(f"Nueva sesión creada ({fecha} {hora_inicio}-{hora_fin}, estado={estado})")
            self.accept()
        except Exception as e:
            log.error(f"Error creando sesión: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo crear la sesión: {e}")


class VistaCalendario(QWidget):
    """
    Vista de calendario: calendario mensual + lista de sesiones del día seleccionado.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        titulo = QLabel("Calendario de sesiones")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 8px;")
        layout.addWidget(titulo)

        # Calendario
        self.calendario = QCalendarWidget()
        self.calendario.selectionChanged.connect(self._fecha_cambiada)
        layout.addWidget(self.calendario)

        # Controles
        controls = QHBoxLayout()
        self.btn_recargar = QPushButton("Recargar")
        self.btn_ir_hoy = QPushButton("Hoy")
        self.btn_nueva = QPushButton("Nueva sesión")
        controls.addWidget(self.btn_recargar)
        controls.addWidget(self.btn_ir_hoy)
        controls.addWidget(self.btn_nueva)
        layout.addLayout(controls)

        # Lista de sesiones
        self.lista_sesiones = QListWidget()
        layout.addWidget(self.lista_sesiones)

        # Conexiones
        self.btn_recargar.clicked.connect(self._cargar_sesiones_seleccion)
        self.btn_ir_hoy.clicked.connect(self._ir_hoy)
        self.btn_nueva.clicked.connect(self._abrir_dialogo_nueva)

        # Carga inicial
        self._cargar_sesiones_seleccion()

    def _formato_fecha(self, qdate: QDate) -> str:
        return qdate.toPyDate().strftime("%Y-%m-%d")

    def _fecha_cambiada(self):
        self._cargar_sesiones_seleccion()

    def _ir_hoy(self):
        hoy = QDate.currentDate()
        self.calendario.setSelectedDate(hoy)
        self._cargar_sesiones_seleccion()

    def _abrir_dialogo_nueva(self):
        fecha_sel = self._formato_fecha(self.calendario.selectedDate())
        dlg = DialogoNuevaSesion(self, fecha_sel)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._cargar_sesiones_seleccion()

    def _cargar_sesiones_seleccion(self):
        self.lista_sesiones.clear()
        fecha = self._formato_fecha(self.calendario.selectedDate())

        if SesionRepository is None:
            self.lista_sesiones.addItem("Repositorio de sesiones no disponible.")
            log.debug("No se puede cargar sesiones: SesionRepository inexistente.")
            return

        try:
            filas = SesionRepository.listar_por_fecha(fecha)
            if not filas:
                self.lista_sesiones.addItem(f"No hay sesiones para {fecha}")
                return

            for f in filas:
                inicio = f.get("hora_inicio", "")
                fin = f.get("hora_fin", "")
                estado = f.get("estado", "").capitalize()
                direccion = f.get("direccion") or "Sin dirección"
                texto = f"[{estado}] {inicio}-{fin} | {direccion}"
                if f.get("notas"):
                    texto += f" — {f['notas'][:60]}"
                self.lista_sesiones.addItem(texto)

            log.info(f"Cargadas {len(filas)} sesiones para {fecha}")
        except Exception as e:
            log.error(f"Error cargando sesiones para {fecha}: {e}")
            QMessageBox.warning(self, "Error", f"No se pudieron cargar sesiones: {e}")

