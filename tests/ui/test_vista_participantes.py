import pytest
from PyQt6.QtWidgets import QApplication
from planificador.ui.vistas.vista_participantes import VistaParticipantes

@pytest.fixture(scope="module")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app

def test_vista_participantes_inicializa(app):
    vista = VistaParticipantes()
    assert vista is not None
    assert vista.tabla is not None
    assert vista.btn_nuevo is not None

def test_vista_participantes_carga_vacia(app, monkeypatch):
    vista = VistaParticipantes()
    monkeypatch.setattr("planificador.data.repositories.cliente_final_repo.ClienteFinalRepository.listar", lambda: [])
    vista.cargar_participantes()
    assert vista.tabla.rowCount() == 0
