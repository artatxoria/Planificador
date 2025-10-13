import os
from pathlib import Path
import pytest
from planificador.data.db_manager import init_db
from planificador.data.repositories.cliente_repo import ClienteRepository
from planificador.data.repositories.tema_repo import TemaRepository
from planificador.data.repositories.formacion_base_repo import FormacionBaseRepository
from planificador.data.repositories.contratacion_repo import ContratacionRepository
from planificador.servicios.servicio_calendario import crear_sesion_validada
from planificador.common.registro import configurar_registro

@pytest.fixture(autouse=True)
def setup_db(tmp_path):
    # Reinicia BD
    init_db(force=True)
    # Configura logging hacia un archivo temporal por test
    log_file = tmp_path / "test.log"
    configurar_registro(archivo=log_file, nivel_texto="DEBUG",
                        max_bytes=200000, copias=1, forzar=True)
    return log_file

def _contratacion_basica():
    cli_id = ClienteRepository.crear("Empresa Log", "B11111111")
    tema_id = TemaRepository.crear("Logística")
    fb_id = FormacionBaseRepository.crear("Excel Intermedio", tema_id)
    c_id = ContratacionRepository.crear(cli_id, fb_id, expediente="EXP-LOG")
    return c_id

def test_logging_creacion_sesion_y_avisos(setup_db):
    log_file = setup_db
    c_id = _contratacion_basica()

    # Crear primera sesión
    crear_sesion_validada(c_id, "2025-11-01", "09:00", "11:00", direccion="Sede A")

    # Intento con margen insuficiente (debería fallar y dejar rastro)
    with pytest.raises(ValueError):
        crear_sesion_validada(c_id, "2025-11-01", "11:15", "12:00", direccion="Sede B")

    # Revisa que el log existe y contiene líneas relevantes
    assert log_file.exists()
    contenido = Path(log_file).read_text(encoding="utf-8")
    assert "Creación de sesión solicitada" in contenido
    assert "Sesión creada con ID" in contenido
    assert "margen insuficiente" in contenido.lower()
