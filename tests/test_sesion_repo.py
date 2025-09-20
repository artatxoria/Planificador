import pytest
from planificador.data.db_manager import init_db
from planificador.data.repositories.cliente_repo import ClienteRepository
from planificador.data.repositories.tema_repo import TemaRepository
from planificador.data.repositories.formacion_base_repo import FormacionBaseRepository
from planificador.data.repositories.contratacion_repo import ContratacionRepository
from planificador.data.repositories.sesion_repo import SesionRepository

@pytest.fixture(autouse=True)
def setup_db():
    init_db(force=True)

def test_crud_sesion():
    cliente_id = ClienteRepository.crear("Empresa Demo", "B12345678")
    tema_id = TemaRepository.crear("Ofimática")
    fb_id = FormacionBaseRepository.crear("Excel Básico", tema_id)
    contratacion_id = ContratacionRepository.crear(cliente_id, fb_id, expediente="EXP-001")

    sesion_id = SesionRepository.crear(contratacion_id, "2025-10-01", "09:00", "12:00")
    sesion = SesionRepository.obtener_por_id(sesion_id)
    assert sesion["hora_inicio"] == "09:00"

    SesionRepository.actualizar(sesion_id, estado="reprogramada")
    sesion = SesionRepository.obtener_por_id(sesion_id)
    assert sesion["estado"] == "reprogramada"

    sesiones = SesionRepository.listar_por_contratacion(contratacion_id)
    assert len(sesiones) == 1

    SesionRepository.borrar(sesion_id)
    assert SesionRepository.obtener_por_id(sesion_id) is None
