import pytest
from planificador.data.db_manager import init_db
from planificador.data.repositories.adjunto_repo import AdjuntoRepository
from planificador.data.repositories.cliente_repo import ClienteRepository

@pytest.fixture(autouse=True)
def setup_db():
    init_db(force=True)

def test_crud_adjunto():
    cliente_id = ClienteRepository.crear("Empresa Demo", "B12345678")
    adj_id = AdjuntoRepository.crear("cliente", cliente_id, "contrato.pdf")

    adj = AdjuntoRepository.obtener_por_id(adj_id)
    assert adj["ruta_fichero"] == "contrato.pdf"

    adjs = AdjuntoRepository.listar_por_origen("cliente", cliente_id)
    assert len(adjs) == 1

    AdjuntoRepository.borrar(adj_id)
    assert AdjuntoRepository.obtener_por_id(adj_id) is None
