import pytest
from planificador.dominio.modelos.adjunto import Adjunto
from planificador.common.registro import configurar_registro

@pytest.fixture(autouse=True)
def setup_logging(tmp_path):
    log_file = tmp_path / "adjunto.log"
    configurar_registro(archivo=log_file, nivel_texto="DEBUG", forzar=True)
    return log_file

def test_logging_adjunto_ok(setup_logging):
    log_file = setup_logging
    Adjunto(origen="cliente", id_origen=1, ruta_fichero="contrato.pdf")
    contenido = log_file.read_text(encoding="utf-8")
    assert "Adjunto" in contenido
    assert "creado" in contenido

def test_logging_adjunto_error(setup_logging):
    log_file = setup_logging
    with pytest.raises(ValueError):
        Adjunto(origen=None, id_origen=1, ruta_fichero="archivo.pdf")
    contenido = log_file.read_text(encoding="utf-8")
    assert "Adjunto" in contenido
    assert "Error" in contenido
