import pytest
from planificador.common.registro import configurar_registro
from planificador.dominio.modelos.cliente import Cliente
from planificador.dominio.modelos.tema import Tema
from planificador.dominio.modelos.formacion_base import FormacionBase
from planificador.dominio.modelos.contratacion import Contratacion
from planificador.dominio.modelos.sesion import Sesion
from planificador.dominio.modelos.adjunto import Adjunto
from planificador.dominio.modelos.interaccion import InteraccionCliente

@pytest.fixture(autouse=True)
def setup_logging(tmp_path):
    log_file = tmp_path / "flujo.log"
    configurar_registro(archivo=log_file, nivel_texto="DEBUG", forzar=True)
    return log_file

def test_flujo_completo_logging(setup_logging):
    log_file = setup_logging

    # 1. Crear un cliente
    c = Cliente(empresa="Empresa X", cif="B99999999", persona_contacto="Juan", email="juan@empresa.com")

    # 2. Crear un tema
    t = Tema(nombre="Python Avanzado")

    # 3. Crear una formación base
    f = FormacionBase(nombre="Curso Python", id_tema=1, horas_referencia=20)

    # 4. Crear una contratación
    ctr = Contratacion(id_cliente=1, id_formacion_base=1, expediente="EXP-2025", precio_hora=50, horas_previstas=20)

    # 5. Crear una sesión
    s = Sesion(id_contratacion=1, fecha="2025-10-15", hora_inicio="09:00", hora_fin="13:00")

    # 6. Crear un adjunto
    a = Adjunto(origen="contratacion", id_origen=1, ruta_fichero="contrato.pdf")

    # 7. Registrar una interacción
    i = InteraccionCliente(id_cliente=1, fecha="2025-09-25", tipo="llamada", descripcion="Contacto inicial")

    # --- Verificar log ---
    contenido = log_file.read_text(encoding="utf-8")

    # Palabras clave esperadas
    assert "Cliente" in contenido
    assert "Tema" in contenido
    assert "FormacionBase" in contenido
    assert "Contratacion" in contenido or "Contratación" in contenido
    assert "Sesion" in contenido or "Sesión" in contenido  # ✅ aceptar ambas formas
    assert "Adjunto" in contenido
    assert "Interaccion" in contenido
