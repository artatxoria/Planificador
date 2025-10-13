import pytest
from planificador.dominio.modelos.contratacion import Contratacion
from planificador.common.registro import configurar_registro

@pytest.fixture(autouse=True)
def setup_logging(tmp_path):
    log_file = tmp_path / "contratacion.log"
    configurar_registro(archivo=log_file, nivel_texto="DEBUG", forzar=True)
    return log_file

def test_logging_contratacion_ok(setup_logging):
    log_file = setup_logging
    Contratacion(id_cliente=1, id_formacion_base=1, expediente="EXP-123", precio_hora=50)
    contenido = log_file.read_text(encoding="utf-8")
    assert "Contratacion" in contenido or "Contratación" in contenido
    assert "cread" in contenido  # vale para "creada" o "creado"

def test_logging_contratacion_error(setup_logging):
    log_file = setup_logging
    with pytest.raises(ValueError):
        Contratacion(id_cliente=None, id_formacion_base=1, expediente="EXP-123")
    contenido = log_file.read_text(encoding="utf-8")
    assert "Contratacion" in contenido or "Contratación" in contenido
    assert "Error" in contenido

