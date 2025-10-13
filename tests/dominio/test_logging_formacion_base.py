import pytest
from planificador.dominio.modelos.formacion_base import FormacionBase
from planificador.common.registro import configurar_registro

@pytest.fixture(autouse=True)
def setup_logging(tmp_path):
    log_file = tmp_path / "formacion.log"
    configurar_registro(archivo=log_file, nivel_texto="DEBUG", forzar=True)
    return log_file

def test_logging_formacion_ok(setup_logging):
    log_file = setup_logging
    FormacionBase(nombre="Excel Básico", id_tema=1, horas_referencia=10)
    contenido = log_file.read_text(encoding="utf-8")
    assert "FormacionBase" in contenido
    assert "creada" in contenido

def test_logging_formacion_error(setup_logging):
    log_file = setup_logging
    with pytest.raises(ValueError):
        FormacionBase(nombre=None, id_tema=1)
    contenido = log_file.read_text(encoding="utf-8")
    assert "FormacionBase" in contenido
    assert "Error" in contenido

