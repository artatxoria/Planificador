import pytest
from planificador.dominio.modelos.cliente import Cliente

def test_cliente_valido():
    cliente = Cliente(empresa="Empresa Demo", cif="B12345678", email="info@demo.com")
    assert cliente.empresa == "Empresa Demo"
    assert cliente.cif == "B12345678"

def test_cliente_sin_empresa_lanza_error():
    with pytest.raises(ValueError):
        Cliente(empresa=None, cif="B12345678")

def test_cliente_email_invalido():
    with pytest.raises(ValueError):
        Cliente(empresa="Empresa X", cif="C98765432", email="correo-invalido")
