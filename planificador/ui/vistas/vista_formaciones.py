# planificador/ui/vistas/vista_formaciones.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QMessageBox, QDialog, QFormLayout, QLineEdit, QTextEdit,
    QSpinBox, QDialogButtonBox, QComboBox
)
from planificador.common.registro import get_logger

log = get_logger(__name__)

try:
    from planificador.data.repositories.formacion_base_repo import FormacionBaseRepository
    from planificador.data.repositories.tema_repo import TemaRepository
except Exception:
    FormacionBaseRepository = None
    TemaRepository = None
    log.warning("FormacionBaseRepository o TemaRepository no disponible en vista_formaciones.")


class DialogoFormacion(QDialog):
    """
    Diálogo modal para crear o editar una FormacionBase.
    Usa FormacionBaseRepository.crear(...) y, si se proporciona id, actualizar(...).
    """

    def __init__(self, parent=None, id_formacion=None):
        super().__init__(parent)
        self.setWindowTitle("Formulario de formación")
        self.id_formacion = id_formacion

        self.layout = QVBoxLayout()
        form = QFormLayout()

        self.input_nombre = QLineEdit()
        form.addRow("Nombre:", self.input_nombre)

        # Tema: combo si hay temas, sino campo libre
        self.combo_tema = QComboBox()
        self.combo_tema.setEditable(False)
        form.addRow("Tema (ID):", self.combo_tema)

        self.input_horas = QSpinBox()
        self.input_horas.setMinimum(0)
        self.input_horas.setMaximum(1000)
        form.addRow("Horas referencia:", self.input_horas)

        self.input_nivel = QLineEdit()
        form.addRow("Nivel:", self.input_nivel)

        self.input_descripcion = QTextEdit()
        self.input_descripcion.setFixedHeight(100)
        form.addRow("Descripción:", self.input_descripcion)

        self.layout.addLayout(form)

        # Botones
        botones = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        botones.accepted.connect(self._guardar)
        botones.rejected.connect(self.reject)
        self.layout.addWidget(botones)

        self.setLayout(self.layout)

        # Carga temas en combo (si el repositorio está disponible)
        self._cargar_temas()

        # Si venimos a editar, cargar valores
        if self.id_formacion:
            self._cargar_datos()

    def _cargar_temas(self):
        self.combo_tema.clear()
        if TemaRepository is None:
            # Si no existe repositorio, permitir escribir ID manualmente
            self.combo_tema.addItem("No hay temas (crear tema primero)")
            self.combo_tema.setEnabled(False)
            log.debug("TemaRepository no disponible en DialogoFormacion.")
            return

        try:
            temas = TemaRepository.listar()
            if not temas:
                self.combo_tema.addItem("Sin temas (crear tema primero)")
                self.combo_tema.setEnabled(False)
                return
            # Guardamos una lista par id->display
            for t in temas:
                label = f"{t['id_tema']} - {t.get('nombre','')}"
                self.combo_tema.addItem(label, t["id_tema"])
        except Exception as e:
            log.error(f"Error cargando temas: {e}")
            self.combo_tema.addItem("Error cargando temas")
            self.combo_tema.setEnabled(False)

    def _cargar_datos(self):
        """Carga los datos de la formación si existe (solo si repositorio lo soporta)."""
        if FormacionBaseRepository is None:
            return
        try:
            fila = FormacionBaseRepository.obtener_por_id(self.id_formacion)
            if not fila:
                return
            self.input_nombre.setText(fila["nombre"])
            if fila.get("id_tema"):
                # Buscar índice con dato
                for i in range(self.combo_tema.count()):
                    data = self.combo_tema.itemData(i)
                    if data == fila["id_tema"]:
                        self.combo_tema.setCurrentIndex(i)
                        break
            self.input_horas.setValue(fila.get("horas_referencia") or 0)
            self.input_nivel.setText(fila.get("nivel") or "")
            self.input_descripcion.setPlainText(fila.get("descripcion") or "")
        except Exception as e:
            log.error(f"Error cargando datos de formación {self.id_formacion}: {e}")

    def _guardar(self):
        """Valida campos mínimos y crea/actualiza la formación."""
        nombre = self.input_nombre.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Validación", "El nombre es obligatorio.")
            return

        # Determinar id_tema si es posible
        id_tema = None
        if TemaRepository is not None and self.combo_tema.isEnabled():
            data = self.combo_tema.currentData()
            if data:
                id_tema = int(data)
        # Si no hay tema disponible, dejamos id_tema = None (repo puede validar)

        horas = int(self.input_horas.value())
        nivel = self.input_nivel.text().strip() or None
        descripcion = self.input_descripcion.toPlainText().strip() or None

        try:
            if FormacionBaseRepository is None:
                raise RuntimeError("Repositorio de formaciones no disponible.")
            if self.id_formacion:
                FormacionBaseRepository.actualizar(self.id_formacion,
                                                  nombre=nombre,
                                                  id_tema=id_tema,
                                                  horas_referencia=horas,
                                                  nivel=nivel,
                                                  descripcion=descripcion)
                log.info(f"Formación {self.id_formacion} actualizada desde UI.")
            else:
                nid = FormacionBaseRepository.crear(nombre=nombre,
                                                   id_tema=id_tema,
                                                   descripcion=descripcion,
                                                   horas_referencia=horas,
                                                   nivel=nivel,
                                                   contenido_base=None)
                log.info(f"Formación creada desde UI: id={nid}")
            self.accept()
        except Exception as e:
            log.error(f"Error guardando formación: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo guardar la formación: {e}")


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
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Tema ID", "Horas ref."])
        layout.addWidget(self.tabla)

        # Botones
        botones = QHBoxLayout()
        self.btn_recargar = QPushButton("Recargar")
        self.btn_nuevo = QPushButton("Nueva formación")
        botones.addWidget(self.btn_recargar)
        botones.addWidget(self.btn_nuevo)
        layout.addLayout(botones)

        self.btn_recargar.clicked.connect(self.cargar_formaciones)
        self.btn_nuevo.clicked.connect(self.abrir_dialogo_nuevo)

        # carga inicial
        self.cargar_formaciones()

        # Doble click para editar (si repositorio disponible)
        self.tabla.cellDoubleClicked.connect(self._editar_desde_tabla)

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
                # Mostrar ID para referencia
                self.tabla.setItem(i, 0, QTableWidgetItem(str(f.get("id_formacion_base") or "")))
                self.tabla.setItem(i, 1, QTableWidgetItem(f.get("nombre") or ""))
                self.tabla.setItem(i, 2, QTableWidgetItem(str(f.get("id_tema") or "")))
                self.tabla.setItem(i, 3, QTableWidgetItem(str(f.get("horas_referencia") or "")))
            self.tabla.resizeColumnsToContents()
            log.info(f"Cargadas {len(filas)} formaciones.")
        except Exception as e:
            log.error(f"Error cargando formaciones: {e}")
            QMessageBox.warning(self, "Error", f"No se pudieron cargar formaciones: {e}")

    def abrir_dialogo_nuevo(self):
        dlg = DialogoFormacion(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.cargar_formaciones()

    def _editar_desde_tabla(self, row, column):
        """Al hacer doble click en una fila intentamos abrir el diálogo para editar esa formación."""
        if FormacionBaseRepository is None:
            QMessageBox.information(self, "Editar", "Repositorio no disponible.")
            return
        try:
            item = self.tabla.item(row, 0)
            if not item:
                return
            id_str = item.text().strip()
            try:
                id_form = int(id_str)
            except ValueError:
                QMessageBox.information(self, "Editar", "ID inválido.")
                return
            dlg = DialogoFormacion(self, id_formacion=id_form)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                self.cargar_formaciones()
        except Exception as e:
            log.error(f"Error al editar formación desde tabla: {e}")
            QMessageBox.warning(self, "Error", f"No se pudo editar la formación: {e}")
