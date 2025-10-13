import pytest
from planificador.dominio.modelos.tema import Tema
from planificador.common.registro import configurar_registro

@pytest.fixture(autouse=True)
def setup_logging(tmp_path):
    log_file = tmp_path / "tema.log"
    configurar_registro(archivo=log_file, nivel_texto="DEBUG", forzar=True)
    return log_file

def test_logging_tema_ok(setup_logging):
    log_file = setup_logging
    Tema(nombre="Ofimática")
    contenido = log_file.read_text(encoding="utf-8")
    assert "Tema" in contenido
    assert "creado" in contenido

def test_logging_tema_error(setup_logging):
    log_file = setup_logging
    with pytest.raises(ValueError):
        Tema(nombre=None)
    contenido = log_file.read_text(encoding="utf-8")
    assert "Tema" in contenido
    assert "Error" in contenido

