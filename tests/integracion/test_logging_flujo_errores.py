import pytest
from planificador.common.registro import configurar_registro
from planificador.dominio.modelos.cliente import Cliente
from planificador.dominio.modelos.sesion import Sesion
from planificador.dominio.modelos.adjunto import Adjunto
from planificador.dominio.modelos.interaccion import InteraccionCliente

@pytest.fixture(autouse=True)
def setup_logging(tmp_path):
    log_file = tmp_path / "flujo_errores.log"
    configurar_registro(archivo=log_file, nivel_texto="DEBUG", forzar=True)
    return log_file

def test_flujo_con_errores_logging(setup_logging):
    log_file = setup_logging

    # 1. Error: Cliente sin empresa
    with pytest.raises(ValueError):
        Cliente(empresa=None, cif="B11111111")

    # 2. Error: Sesión con horas inválidas
    with pytest.raises(ValueError):
        Sesion(id_contratacion=1, fecha="2025-10-20", hora_inicio="15:00", hora_fin="09:00")

    # 3. Error: Adjunto sin ruta de fichero
    with pytest.raises(ValueError):
        Adjunto(origen="cliente", id_origen=1, ruta_fichero=None)

    # 4. Error: Interacción con tipo inválido
    with pytest.raises(ValueError):
        InteraccionCliente(id_cliente=1, fecha="2025-09-25", tipo="whatsapp")

    # --- Verificar log ---
    contenido = log_file.read_text(encoding="utf-8")

    assert "Cliente" in contenido and "Error" in contenido
    assert "Sesion" in contenido or "Sesión" in contenido
    assert "Adjunto" in contenido and "Error" in contenido
    assert "Interaccion" in contenido and "Error" in contenido
