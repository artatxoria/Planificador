import pytest
from planificador.data.db_manager import init_db
from planificador.data.repositories.cliente_repo import ClienteRepository
from planificador.data.repositories.tema_repo import TemaRepository
from planificador.data.repositories.formacion_base_repo import FormacionBaseRepository
from planificador.data.repositories.contratacion_repo import ContratacionRepository

@pytest.fixture(autouse=True)
def setup_db():
    init_db(force=True)

def test_crud_contratacion():
    cliente_id = ClienteRepository.crear("Empresa Demo", "B12345678")
    tema_id = TemaRepository.crear("Ofimática")
    fb_id = FormacionBaseRepository.crear("Excel Básico", tema_id)
    contratacion_id = ContratacionRepository.crear(cliente_id, fb_id, expediente="EXP-001")

    contratacion = ContratacionRepository.obtener_por_id(contratacion_id)
    assert contratacion["expediente"] == "EXP-001"

    ContratacionRepository.actualizar(contratacion_id, estado="confirmado")
    contratacion = ContratacionRepository.obtener_por_id(contratacion_id)
    assert contratacion["estado"] == "confirmado"

    contrataciones = ContratacionRepository.listar()
    assert len(contrataciones) == 1

    ContratacionRepository.borrar(contratacion_id)
    assert ContratacionRepository.obtener_por_id(contratacion_id) is None
