import pytest
from planificador.data.db_manager import init_db
from planificador.data.repositories.tema_repo import TemaRepository

@pytest.fixture(autouse=True)
def setup_db():
    init_db(force=True)

def test_crud_tema():
    tema_id = TemaRepository.crear("Ofimática", "Cursos de ofimática")
    tema = TemaRepository.obtener_por_id(tema_id)
    assert tema["nombre"] == "Ofimática"

    TemaRepository.actualizar(tema_id, descripcion="Ofimática general")
    tema = TemaRepository.obtener_por_id(tema_id)
    assert tema["descripcion"] == "Ofimática general"

    temas = TemaRepository.listar()
    assert len(temas) == 1

    TemaRepository.borrar(tema_id)
    assert TemaRepository.obtener_por_id(tema_id) is None
