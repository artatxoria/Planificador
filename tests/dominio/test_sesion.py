# tests/dominio/test_sesion.py (Versión corregida probable)
import pytest
from planificador.dominio.modelos.sesion import Sesion

def test_sesion_valida():
    # Este ya pasa, no se toca.
    sesion = Sesion(id_contratacion=1, fecha="2025-10-01", hora_inicio="09:00", hora_fin="11:00", estado="programada")
    assert sesion.id_contratacion == 1

def test_sesion_sin_fecha():
    # Esperamos un ValueError con un mensaje específico sobre la fecha.
    with pytest.raises(ValueError, match="La sesión debe tener una fecha"):
        # Forzamos la validación con estado="programada"
        Sesion(id_contratacion=1, fecha=None, hora_inicio="09:00", hora_fin="11:00", estado="programada")

def test_sesion_sin_hora_inicio():
    # Esperamos un ValueError con un mensaje sobre las horas.
    with pytest.raises(ValueError, match="La sesión debe tener hora de inicio y hora de fin"):
        # Forzamos la validación con estado="programada"
        Sesion(id_contratacion=1, fecha="2025-10-01", hora_inicio=None, hora_fin="11:00", estado="programada")
