import pytest
from planificador.data.db_manager import init_db
from planificador.data.repositories.cliente_repo import ClienteRepository

@pytest.fixture(autouse=True)
def setup_db():
    init_db(force=True)

def test_crud_cliente():
    # Crear
    cliente_id = ClienteRepository.crear("Empresa Demo", "B12345678")
    assert cliente_id is not None

    # Obtener
    cliente = ClienteRepository.obtener_por_id(cliente_id)
    assert cliente["empresa"] == "Empresa Demo"

    # Actualizar
    ClienteRepository.actualizar(cliente_id, empresa="Empresa Modificada")
    cliente = ClienteRepository.obtener_por_id(cliente_id)
    assert cliente["empresa"] == "Empresa Modificada"

    # Listar
    clientes = ClienteRepository.listar()
    assert len(clientes) == 1

    # Borrar
    ClienteRepository.borrar(cliente_id)
    assert ClienteRepository.obtener_por_id(cliente_id) is None
