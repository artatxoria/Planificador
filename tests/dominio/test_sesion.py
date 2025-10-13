import pytest
from planificador.dominio.modelos.sesion import Sesion

def test_sesion_valida():
    s = Sesion(id_contratacion=1, fecha="2025-10-01", hora_inicio="09:00", hora_fin="12:00")
    assert s.hora_inicio == "09:00"
    assert s.hora_fin == "12:00"

def test_sesion_sin_fecha():
    with pytest.raises(ValueError):
        Sesion(id_contratacion=1, fecha=None, hora_inicio="09:00", hora_fin="12:00")

def test_sesion_sin_hora_inicio():
    with pytest.raises(ValueError):
        Sesion(id_contratacion=1, fecha="2025-10-01", hora_inicio=None, hora_fin="12:00")
