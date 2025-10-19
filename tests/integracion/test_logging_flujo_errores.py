import pytest
from planificador.common.registro import configurar_registro
from planificador.dominio.modelos.cliente import Cliente
from planificador.dominio.modelos.sesion import Sesion
from planificador.dominio.modelos.adjunto import Adjunto
from planificador.dominio.modelos.interaccion import InteraccionCliente

@pytest.fixture(autouse=True)
def setup_logging(tmp_path):
    """
    Configura el logging para cada test, dirigiendo la salida a un fichero temporal.
    Esto aísla los logs de cada prueba.
    """
    log_file = tmp_path / "flujo_errores.log"
    configurar_registro(archivo=log_file, nivel_texto="DEBUG", forzar=True)
    return log_file

def test_flujo_con_errores_logging(setup_logging):
    """
    Verifica que los errores de validación en los modelos de dominio
    lanzan las excepciones correctas y son registrados en el log.
    """
    log_file = setup_logging

    # 1. Error: Cliente sin empresa.
    with pytest.raises(ValueError, match="El campo 'empresa' es obligatorio"):
        Cliente(empresa=None, cif="B11111111")

    # 2. Error: Sesión con horas inválidas.
    with pytest.raises(ValueError, match="La hora de inicio debe ser anterior a la de fin"):
        Sesion(
            id_contratacion=1,
            fecha="2025-10-20",
            hora_inicio="15:00",
            hora_fin="09:00",
            estado="programada"
        )

    # 3. Error: Adjunto sin ruta de fichero.
    with pytest.raises(ValueError, match="El adjunto debe tener una ruta de fichero válida"):
        Adjunto(origen="cliente", id_origen=1, ruta_fichero=None)

    # 4. Error: Interacción con tipo inválido.
    # El mensaje real es "El tipo de interacción debe ser uno de {...}".
    # Usamos una expresión regular flexible con `.*` para evitar problemas con el orden del set.
    with pytest.raises(ValueError, match=r"El tipo de interacción debe ser uno de .*"):
        InteraccionCliente(id_cliente=1, fecha="2025-09-25", tipo="whatsapp")

    # --- Verificar log ---
    contenido = log_file.read_text(encoding="utf-8")

    assert "Error al crear Cliente: falta 'empresa'" in contenido
    assert "Horas inválidas en Sesion" in contenido
    assert "Error al crear Adjunto: falta 'ruta_fichero'" in contenido
    # El log real es "Tipo inválido en InteraccionCliente: whatsapp"
    assert "Tipo inválido en InteraccionCliente: whatsapp" in contenido

