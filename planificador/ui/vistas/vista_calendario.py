from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCalendarWidget, QListWidget, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import QDate
from datetime import datetime
from planificador.common.registro import get_logger

log = get_logger(__name__)

try:
    from planificador.data.repositories.sesion_repo import SesionRepository
except Exception:
    SesionRepository = None
    log.warning("SesionRepository no disponible en vista_calendario.")


class VistaCalendario(QWidget):
    """
    Vista de calendario: calendario mensual + lista de sesiones del día seleccionado.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        titulo = QLabel("Calendario")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 8px;")
        layout.addWidget(titulo)

        # Calendario
        self.calendario = QCalendarWidget()
        self.calendario.selectionChanged.connect(self._fecha_cambiada)
        layout.addWidget(self.calendario)

        # Controles y lista de sesiones
        controls = QHBoxLayout()
        self.btn_recargar = QPushButton("Recargar sesiones")
        self.btn_ir_hoy = QPushButton("Ir a hoy")
        controls.addWidget(self.btn_recargar)
        controls.addWidget(self.btn_ir_hoy)
        layout.addLayout(controls)

        self.lista_sesiones = QListWidget()
        layout.addWidget(self.lista_sesiones)

        self.btn_recargar.clicked.connect(self._cargar_sesiones_seleccion)
        self.btn_ir_hoy.clicked.connect(self._ir_hoy)

        # Carga inicial
        self._cargar_sesiones_seleccion()

    def _formato_fecha(self, qdate: QDate) -> str:
        pydate = qdate.toPyDate()
        return pydate.strftime("%Y-%m-%d")

    def _fecha_cambiada(self):
        self._cargar_sesiones_seleccion()

    def _ir_hoy(self):
        hoy = QDate.currentDate()
        self.calendario.setSelectedDate(hoy)
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
                # Mostrar cliente/expediente si está disponible
                texto = f"{inicio}-{fin} | {f.get('direccion') or 'Sin dirección'}"
                if f.get("notas"):
                    texto += f" — {f.get('notas')[:60]}"
                self.lista_sesiones.addItem(texto)

            log.info(f"Cargadas {len(filas)} sesiones para {fecha}")
        except Exception as e:
            log.error(f"Error cargando sesiones para {fecha}: {e}")
            QMessageBox.warning(self, "Error", f"No se pudieron cargar sesiones: {e}")
