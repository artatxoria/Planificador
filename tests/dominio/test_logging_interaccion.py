import pytest
from planificador.dominio.modelos.interaccion import InteraccionCliente
from planificador.common.registro import configurar_registro

@pytest.fixture(autouse=True)
def setup_logging(tmp_path):
    log_file = tmp_path / "interaccion.log"
    configurar_registro(archivo=log_file, nivel_texto="DEBUG", forzar=True)
    return log_file

def test_logging_interaccion_ok(setup_logging):
    log_file = setup_logging
    i = InteraccionCliente(id_cliente=1, fecha="2025-09-20", tipo="email", descripcion="Prueba")
    _ = i.requiere_recordatorio()
    contenido = log_file.read_text(encoding="utf-8")
    assert "Interaccion" in contenido  # más genérico
    assert "creada" in contenido or "requiere_recordatorio" in contenido


def test_logging_interaccion_error(setup_logging):
    log_file = setup_logging
    with pytest.raises(ValueError):
        InteraccionCliente(id_cliente=1, fecha="2025-09-20", tipo="invalido")
    contenido = log_file.read_text(encoding="utf-8")
    assert "InteraccionCliente" in contenido
    assert "Error" in contenido or "inválido" in contenido or "invalido" in contenido
