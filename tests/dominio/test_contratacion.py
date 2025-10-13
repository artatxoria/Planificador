import pytest
from planificador.dominio.modelos.contratacion import Contratacion

def test_contratacion_valida():
    c = Contratacion(id_cliente=1, id_formacion_base=2, expediente="EXP-001", precio_hora=50)
    assert c.expediente == "EXP-001"
    assert c.precio_hora == 50

def test_contratacion_sin_cliente():
    with pytest.raises(ValueError):
        Contratacion(id_cliente=None, id_formacion_base=1, expediente="EXP-002")

def test_contratacion_precio_invalido():
    with pytest.raises(ValueError):
        Contratacion(id_cliente=1, id_formacion_base=1, expediente="EXP-003", precio_hora=0)
