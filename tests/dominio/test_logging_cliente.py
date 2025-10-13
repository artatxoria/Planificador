import pytest
from planificador.dominio.modelos.cliente import Cliente
from planificador.common.registro import configurar_registro

@pytest.fixture(autouse=True)
def setup_logging(tmp_path):
    log_file = tmp_path / "cliente.log"
    configurar_registro(archivo=log_file, nivel_texto="DEBUG", forzar=True)
    return log_file

def test_logging_cliente_ok(setup_logging):
    log_file = setup_logging
    Cliente(empresa="Empresa Test", cif="B12345678", email="test@demo.com")
    contenido = log_file.read_text(encoding="utf-8")
    assert "Cliente" in contenido
    assert "creado" in contenido

def test_logging_cliente_error(setup_logging):
    log_file = setup_logging
    with pytest.raises(ValueError):
        Cliente(empresa=None, cif="B12345678")
    contenido = log_file.read_text(encoding="utf-8")
    assert "Cliente" in contenido
    assert "Error" in contenido

