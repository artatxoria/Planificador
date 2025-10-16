from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QListWidget,
    QStackedWidget, QHBoxLayout, QMenuBar, QStatusBar, QMessageBox
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import sys

# Importar todas las vistas existentes
from planificador.ui.vistas.vista_clientes import VistaClientes
from planificador.ui.vistas.vista_calendario import VistaCalendario
from planificador.ui.vistas.vista_formaciones import VistaFormaciones
from planificador.ui.vistas.vista_interacciones import VistaInteracciones
from planificador.ui.vistas.vista_configuracion import VistaConfiguracion
from planificador.ui.vistas.vista_recordatorios import VistaRecordatorios  # ✅ NUEVA

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Planificador de Formaciones")
        self.resize(1250, 850)

        # --- Menú superior ---
        self._crear_menu()

        # --- Panel lateral + contenido central ---
        contenedor = QWidget()
        layout = QHBoxLayout(contenedor)

        self.menu_lateral = QListWidget()
        self.menu_lateral.addItems([
            "Clientes",
            "Calendario",
            "Formaciones",
            "Interacciones",
            "Recordatorios",   # ✅ Nuevo apartado
            "Configuración",
        ])
        self.menu_lateral.setMaximumWidth(220)
        self.menu_lateral.currentRowChanged.connect(self._cambiar_vista)

        # --- Vistas ---
        self.vistas = QStackedWidget()
        self.vistas.addWidget(VistaClientes())
        self.vistas.addWidget(VistaCalendario())
        self.vistas.addWidget(VistaFormaciones())
        self.vistas.addWidget(VistaInteracciones())
        self.vistas.addWidget(VistaRecordatorios())  # ✅ Nueva vista insertada
        self.vistas.addWidget(VistaConfiguracion())

        layout.addWidget(self.menu_lateral)
        layout.addWidget(self.vistas, 1)

        self.setCentralWidget(contenedor)
        self.setStatusBar(QStatusBar())

    # ----------------------------------------------------------------------
    # Menú superior
    # ----------------------------------------------------------------------
    def _crear_menu(self):
        barra_menu = self.menuBar()

        menu_archivo = barra_menu.addMenu("Archivo")
        salir = QAction("Salir", self)
        salir.triggered.connect(self.close)
        menu_archivo.addAction(salir)

        menu_ver = barra_menu.addMenu("Ver")
        menu_ayuda = barra_menu.addMenu("Ayuda")

        acerca_de = QAction("Acerca de", self)
        acerca_de.triggered.connect(self._mostrar_acerca_de)
        menu_ayuda.addAction(acerca_de)

    # ----------------------------------------------------------------------
    # Cambiar vista en el panel principal
    # ----------------------------------------------------------------------
    def _cambiar_vista(self, indice):
        self.vistas.setCurrentIndex(indice)

    # ----------------------------------------------------------------------
    # Acerca de
    # ----------------------------------------------------------------------
    def _mostrar_acerca_de(self):
        QMessageBox.information(
            self,
            "Acerca de",
            "Planificador de Formaciones\n"
            "Desarrollado por Juan Carlos Beaskoetxea\n"
            "© 2025 — con integración de Recordatorios"
        )


def main():
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
