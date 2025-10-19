import pytest
from PyQt6.QtWidgets import QApplication
from planificador.ui.vistas.vista_contactos_clientes_finales import VistaContactosClientesFinales

@pytest.fixture(scope="module")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app

def test_vista_inicializa(app):
    vista = VistaContactosClientesFinales()
    assert vista is not None
    assert vista.tabla is not None
    assert vista.btn_nuevo is not None

def test_cargar_contactos_vacia(app, monkeypatch):
    vista = VistaContactosClientesFinales()
    monkeypatch.setattr("planificador.data.repositories.cliente_final_repo.ClienteFinalRepository.listar", lambda: [])
    vista.cargar_contactos()
    assert vista.tabla.rowCount() == 0
