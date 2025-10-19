import pytest
from pathlib import Path
from planificador.common.registro import configurar_registro
from planificador.dominio.modelos.sesion import Sesion

@pytest.fixture(autouse=True)
def setup_logging(tmp_path: Path) -> Path:
    """
    Configura un logger aislado para cada test, escribiendo en un fichero temporal.
    Devuelve la ruta al fichero de log para poder verificar su contenido.
    """
    log_file = tmp_path / "sesion.log"
    configurar_registro(archivo=log_file, nivel_texto="DEBUG", forzar=True)
    return log_file

def test_logging_sesion_ok(setup_logging: Path):
    """
    Verifica que la creación de una Sesión válida se registra correctamente en el log.
    """
    log_file = setup_logging
    
    # Creamos una sesión válida para asegurar que el logging funciona en el caso de éxito.
    Sesion(
        id_contratacion=1, 
        fecha="2025-10-01", 
        hora_inicio="09:00", 
        hora_fin="11:00", 
        estado="programada"  # Usamos un estado que active la validación
    )
    
    contenido = log_file.read_text(encoding="utf-8")
    
    # Verificamos que se han registrado los mensajes informativos esperados.
    assert "Sesión creada" in contenido
    assert "INFO" in contenido
    assert "programada" in contenido
    assert "ERROR" not in contenido

def test_logging_sesion_error(setup_logging: Path):
    """
    Verifica que la creación de una Sesión con datos inválidos
    lanza un ValueError y registra un mensaje de ERROR.
    """
    log_file = setup_logging
    
    # 1. Verificamos que se lanza la excepción correcta con el mensaje esperado.
    with pytest.raises(ValueError, match="La hora de inicio debe ser anterior a la de fin"):
        # Creamos una sesión con horas inválidas y un estado que fuerce la validación.
        Sesion(
            id_contratacion=1, 
            fecha="2025-10-01", 
            hora_inicio="12:00", 
            hora_fin="10:00",  # <-- Horas inválidas
            estado="programada"  # <-- La clave para forzar la validación
        )
        
    # 2. Verificamos que el log de error se ha escrito correctamente.
    contenido = log_file.read_text(encoding="utf-8")
    
    assert "ERROR" in contenido
    assert "Horas inválidas en Sesion" in contenido

