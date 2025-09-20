import pytest
from planificador.data.db_manager import init_db
from planificador.data.repositories.tema_repo import TemaRepository
from planificador.data.repositories.formacion_base_repo import FormacionBaseRepository

@pytest.fixture(autouse=True)
def setup_db():
    init_db(force=True)

def test_crud_formacion_base():
    tema_id = TemaRepository.crear("Ofimática")
    fb_id = FormacionBaseRepository.crear("Excel Básico", tema_id, nivel="basico")
    fb = FormacionBaseRepository.obtener_por_id(fb_id)
    assert fb["nombre"] == "Excel Básico"

    FormacionBaseRepository.actualizar(fb_id, nombre="Excel Avanzado")
    fb = FormacionBaseRepository.obtener_por_id(fb_id)
    assert fb["nombre"] == "Excel Avanzado"

    formaciones = FormacionBaseRepository.listar()
    assert len(formaciones) == 1

    FormacionBaseRepository.borrar(fb_id)
    assert FormacionBaseRepository.obtener_por_id(fb_id) is None
