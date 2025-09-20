import pytest
from planificador.data.db_manager import init_db
from planificador.data.repositories.cliente_repo import ClienteRepository
from planificador.data.repositories.tema_repo import TemaRepository
from planificador.data.repositories.formacion_base_repo import FormacionBaseRepository
from planificador.data.repositories.contratacion_repo import ContratacionRepository
from planificador.data.repositories.sesion_repo import SesionRepository
from planificador.data.repositories.interaccion_repo import InteraccionRepository
from planificador.data.repositories.adjunto_repo import AdjuntoRepository

@pytest.fixture(autouse=True)
def setup_db():
    init_db(force=True)

def test_flujo_completo():
    # 1. Crear cliente
    cliente_id = ClienteRepository.crear("Empresa Demo", "B12345678", persona_contacto="Juan Pérez")
    cliente = ClienteRepository.obtener_por_id(cliente_id)
    assert cliente["empresa"] == "Empresa Demo"

    # 2. Crear tema
    tema_id = TemaRepository.crear("Ofimática", "Cursos de ofimática")
    tema = TemaRepository.obtener_por_id(tema_id)
    assert tema["nombre"] == "Ofimática"

    # 3. Crear formación base
    fb_id = FormacionBaseRepository.crear("Excel Básico", tema_id, horas_referencia=20, nivel="basico")
    fb = FormacionBaseRepository.obtener_por_id(fb_id)
    assert fb["nombre"] == "Excel Básico"

    # 4. Crear contratación
    contratacion_id = ContratacionRepository.crear(
        cliente_id, fb_id, expediente="EXP-0001", precio_hora=50, horas_previstas=20, modalidad="presencial"
    )
    contratacion = ContratacionRepository.obtener_por_id(contratacion_id)
    assert contratacion["expediente"] == "EXP-0001"

    # 5. Crear sesión
    sesion_id = SesionRepository.crear(contratacion_id, "2025-10-01", "09:00", "12:00", direccion="Oficinas cliente")
    sesion = SesionRepository.obtener_por_id(sesion_id)
    assert sesion["direccion"] == "Oficinas cliente"

    # 6. Crear interacción
    inter_id = InteraccionRepository.crear(
        id_cliente=cliente_id,
        fecha="2025-09-21",
        tipo="llamada",
        descripcion="Llamada para confirmar agenda",
        resultado="pendiente",
        proxima_accion="Enviar confirmación por email",
        fecha_proxima_accion="2025-09-22",
        crear_recordatorio=1
    )
    interaccion = InteraccionRepository.obtener_por_id(inter_id)
    assert interaccion["tipo"] == "llamada"

    # 7. Crear adjunto
    adj_id = AdjuntoRepository.crear("cliente", cliente_id, "contrato.pdf", tipo="pdf")
    adj = AdjuntoRepository.obtener_por_id(adj_id)
    assert adj["ruta_fichero"] == "contrato.pdf"

    # 8. Validaciones cruzadas
    contrataciones = ContratacionRepository.listar()
    assert len(contrataciones) == 1

    sesiones = SesionRepository.listar_por_contratacion(contratacion_id)
    assert len(sesiones) == 1

    interacciones = InteraccionRepository.listar_por_cliente(cliente_id)
    assert len(interacciones) == 1

    adjuntos = AdjuntoRepository.listar_por_origen("cliente", cliente_id)
    assert len(adjuntos) == 1
