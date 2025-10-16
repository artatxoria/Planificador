import pytest
from PyQt6.QtWidgets import QApplication
from planificador.ui.vistas.vista_recordatorios import VistaRecordatorios

@pytest.fixture(scope="module")
def app():
    """Crea una instancia única de QApplication para los tests PyQt."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


def test_vista_recordatorios_inicializa(app):
    """Verifica que la vista se inicializa sin errores y contiene los elementos esperados."""
    vista = VistaRecordatorios()
    assert vista is not None
    assert vista.windowTitle() == ""  # No debe tener título de ventana propio
    assert vista.tabla is not None
    assert vista.btn_recargar is not None
    assert vista.btn_generar is not None


def test_vista_recordatorios_carga_vacia(app, monkeypatch):
    """Verifica que la vista muestra un mensaje cuando no hay recordatorios."""
    vista = VistaRecordatorios()

    # Simula un repositorio vacío
    monkeypatch.setattr("planificador.data.repositories.recordatorio_repo.RecordatorioRepository.listar_todos", lambda: [])

    vista.cargar_recordatorios()

    # Debe dejar la tabla vacía (0 filas)
    assert vista.tabla.rowCount() == 0


def test_vista_recordatorios_carga_datos(app, monkeypatch):
    """Verifica que los datos se muestran correctamente en la tabla."""
    vista = VistaRecordatorios()

    mock_datos = [
        {
            "tipo": "llamada",
            "cliente": "Cliente Demo",
            "fecha": "2025-10-15",
            "descripcion": "Llamar para confirmar sesión",
        },
        {
            "tipo": "reunión",
            "cliente": "Empresa XYZ",
            "fecha": "2025-10-16",
            "descripcion": "Presentar propuesta de formación",
        },
    ]

    monkeypatch.setattr("planificador.data.repositories.recordatorio_repo.RecordatorioRepository.listar_todos", lambda: mock_datos)

    vista.cargar_recordatorios()

    assert vista.tabla.rowCount() == 2
    assert vista.tabla.item(0, 0).text() == "llamada"
    assert "Empresa" in vista.tabla.item(1, 1).text()
