import pytest
from planificador.data.db_manager import init_db
from planificador.data.repositories.cliente_repo import ClienteRepository
from planificador.data.repositories.interaccion_repo import InteraccionRepository

@pytest.fixture(autouse=True)
def setup_db():
    init_db(force=True)

def test_crud_interaccion():
    cliente_id = ClienteRepository.crear("Empresa Demo", "B12345678")
    inter_id = InteraccionRepository.crear(
        id_cliente=cliente_id,
        fecha="2025-09-20",
        tipo="email",
        descripcion="Envío de propuesta"
    )

    inter = InteraccionRepository.obtener_por_id(inter_id)
    assert inter["tipo"] == "email"

    InteraccionRepository.actualizar(inter_id, resultado="aceptado")
    inter = InteraccionRepository.obtener_por_id(inter_id)
    assert inter["resultado"] == "aceptado"

    interacciones = InteraccionRepository.listar_por_cliente(cliente_id)
    assert len(interacciones) == 1

    InteraccionRepository.borrar(inter_id)
    assert InteraccionRepository.obtener_por_id(inter_id) is None
