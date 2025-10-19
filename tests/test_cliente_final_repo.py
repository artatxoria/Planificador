import pytest
from planificador.data.repositories.cliente_final_repo import ClienteFinalRepository
from planificador.data.db_manager import get_connection

def limpiar_tabla():
    with get_connection() as conn:
        conn.execute("DELETE FROM ClienteFinal")
        conn.commit()

@pytest.fixture(autouse=True)
def setup_db():
    limpiar_tabla()
    yield
    limpiar_tabla()

def test_crear_y_obtener_cliente_final():
    id_cf = ClienteFinalRepository.crear(empresa="Empresa Final S.A.", persona_encargada="Ana López", telefono_encargada="600123456", email_encargada="ana@empresa.com")
    assert id_cf is not None

    registro = ClienteFinalRepository.obtener_por_id(id_cf)
    assert registro["empresa"] == "Empresa Final S.A."
    assert registro["persona_encargada"] == "Ana López"

def test_listar_clientes_finales():
    ClienteFinalRepository.crear(empresa="Alpha", persona_encargada="Luis")
    ClienteFinalRepository.crear(empresa="Beta", persona_encargada="María")
    lista = ClienteFinalRepository.listar()
    assert len(lista) == 2

def test_actualizar_cliente_final():
    id_cf = ClienteFinalRepository.crear(empresa="Empresa A", persona_encargada="Inicial")
    ClienteFinalRepository.actualizar(id_cf, persona_encargada="Actualizada")
    registro = ClienteFinalRepository.obtener_por_id(id_cf)
    assert registro["persona_encargada"] == "Actualizada"
