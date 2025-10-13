from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QListWidget,
    QStackedWidget, QHBoxLayout, QMenuBar, QStatusBar, QMessageBox
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import sys

from planificador.ui.vistas.vista_clientes import VistaClientes
from planificador.ui.vistas.vista_calendario import VistaCalendario
from planificador.ui.vistas.vista_formaciones import VistaFormaciones
from planificador.ui.vistas.vista_interacciones import VistaInteracciones
from planificador.ui.vistas.vista_configuracion import VistaConfiguracion


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Planificador de Formaciones")
        self.resize(1200, 800)

        # --- Menú superior ---
        self._crear_menu()

        # --- Panel lateral y contenido central ---
        contenedor = QWidget()
        layout = QHBoxLayout(contenedor)

        self.menu_lateral = QListWidget()
        self.menu_lateral.addItems([
            "Clientes", "Calendario", "Formaciones", "Interacciones", "Configuración"
        ])
        self.menu_lateral.setMaximumWidth(200)
        self.menu_lateral.currentRowChanged.connect(self._cambiar_vista)

        self.vistas = QStackedWidget()
        self.vistas.addWidget(VistaClientes())
        self.vistas.addWidget(VistaCalendario())
        self.vistas.addWidget(VistaFormaciones())
        self.vistas.addWidget(VistaInteracciones())
        self.vistas.addWidget(VistaConfiguracion())

        layout.addWidget(self.menu_lateral)
        layout.addWidget(self.vistas, 1)

        self.setCentralWidget(contenedor)
        self.setStatusBar(QStatusBar())

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

    def _cambiar_vista(self, indice):
        self.vistas.setCurrentIndex(indice)

    def _mostrar_acerca_de(self):
        QMessageBox.information(
            self,
            "Acerca de",
            "Planificador de Formaciones\nDesarrollado por Juan Carlos Beaskoetxea\n© 2025"
        )


def main():
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
