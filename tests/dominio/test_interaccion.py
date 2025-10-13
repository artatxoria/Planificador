import pytest
from planificador.dominio.modelos.adjunto import Adjunto

def test_adjunto_valido():
    a = Adjunto(origen="cliente", id_origen=1, ruta_fichero="contrato.pdf")
    assert a.ruta_fichero == "contrato.pdf"

def test_adjunto_sin_origen():
    with pytest.raises(ValueError):
        Adjunto(origen=None, id_origen=1, ruta_fichero="doc.pdf")

def test_adjunto_sin_ruta():
    with pytest.raises(ValueError):
        Adjunto(origen="cliente", id_origen=1, ruta_fichero=None)
