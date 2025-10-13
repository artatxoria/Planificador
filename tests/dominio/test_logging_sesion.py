import pytest
from planificador.dominio.modelos.sesion import Sesion
from planificador.common.registro import configurar_registro

@pytest.fixture(autouse=True)
def setup_logging(tmp_path):
    log_file = tmp_path / "sesion.log"
    configurar_registro(archivo=log_file, nivel_texto="DEBUG", forzar=True)
    return log_file

def test_logging_sesion_ok(setup_logging):
    log_file = setup_logging
    s = Sesion(id_contratacion=1, fecha="2025-10-01", hora_inicio="09:00", hora_fin="11:00")
    _ = s.duracion_horas()
    contenido = log_file.read_text(encoding="utf-8")
    assert "Sesion" in contenido
    assert "creada" in contenido
    assert "duración" in contenido or "duracion" in contenido

def test_logging_sesion_error(setup_logging):
    log_file = setup_logging
    with pytest.raises(ValueError):
        Sesion(id_contratacion=1, fecha="2025-10-01", hora_inicio="11:00", hora_fin="09:00")
    contenido = log_file.read_text(encoding="utf-8")
    assert "Sesion" in contenido
    assert "Error" in contenido or "inválida" in contenido or "invalida" in contenido


