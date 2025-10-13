import pytest
from planificador.dominio.modelos.formacion_base import FormacionBase

def test_formacion_base_valida():
    fb = FormacionBase(nombre="Excel Básico", id_tema=1, horas_referencia=20)
    assert fb.nombre == "Excel Básico"
    assert fb.horas_referencia == 20

def test_formacion_base_sin_nombre():
    with pytest.raises(ValueError):
        FormacionBase(nombre=None, id_tema=1)

def test_formacion_base_horas_invalidas():
    with pytest.raises(ValueError):
        FormacionBase(nombre="Excel Avanzado", id_tema=1, horas_referencia=0)
