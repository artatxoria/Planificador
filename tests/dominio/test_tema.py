import pytest
from planificador.dominio.modelos.tema import Tema

def test_tema_valido():
    tema = Tema(nombre="Ofimática")
    assert tema.nombre == "Ofimática"

def test_tema_sin_nombre():
    with pytest.raises(ValueError):
        Tema(nombre=None)
