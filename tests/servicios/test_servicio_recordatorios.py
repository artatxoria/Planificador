# tests/servicios/test_servicio_recordatorios.py
import pytest
from datetime import datetime, timedelta
from planificador.data.db_manager import init_db
from planificador.data.repositories.cliente_repo import ClienteRepository
from planificador.data.repositories.interaccion_repo import InteraccionRepository
from planificador.data.repositories.sesion_repo import SesionRepository
from planificador.data.repositories.formacion_base_repo import FormacionBaseRepository
from planificador.data.repositories.contratacion_repo import ContratacionRepository
from planificador.data.repositories.tema_repo import TemaRepository
from planificador.servicios.servicio_recordatorios import ServicioRecordatorios


@pytest.fixture(autouse=True)
def setup_db():
    """
    Inicializa la base de datos antes de cada test
    con un cliente, un tema y una formación base válidos.
    """
    init_db(force=True)
    ClienteRepository.crear("Cliente Demo", "B00000000")
    id_tema = TemaRepository.crear("Tema Prueba", "Tema de ejemplo para tests")
    FormacionBaseRepository.crear("Formación Demo", id_tema=id_tema, horas_referencia=10)


def test_generar_desde_interacciones(tmp_path):
    InteraccionRepository.crear(
        id_cliente=1,
        fecha="2025-10-10",
        tipo="llamada",
        descripcion="Contacto inicial",
        resultado="propuesta",
        proxima_accion="Enviar propuesta",
        fecha_proxima_accion=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        crear_recordatorio=True,
    )

    InteraccionRepository.crear(
        id_cliente=1,
        fecha="2025-10-09",
        tipo="email",
        descripcion="Correo de seguimiento",
        resultado="sin_respuesta",
        proxima_accion=None,
        fecha_proxima_accion=None,
        crear_recordatorio=False,
    )

    recordatorios = ServicioRecordatorios.generar_desde_interacciones()
    assert len(recordatorios) == 1
    assert recordatorios[0]["cliente"] == 1
    assert "Enviar propuesta" in recordatorios[0]["descripcion"]


def test_comprobar_sesiones_proximas(tmp_path):
    # Crear una contratación válida (vincula cliente y formacion base)
    c_id = ContratacionRepository.crear(
        id_cliente=1,
        id_formacion_base=1,
        expediente="EXP-001",
        precio_hora=40,
        horas_previstas=8,
        modalidad="presencial"
    )

    # Usar estado permitido por el esquema: "programada o propuesta"
    SesionRepository.crear(
        id_contratacion=c_id,
        fecha=(datetime.now() + timedelta(hours=20)).strftime("%Y-%m-%d"),
        hora_inicio=(datetime.now() + timedelta(hours=20)).strftime("%H:%M"),
        hora_fin=(datetime.now() + timedelta(hours=22)).strftime("%H:%M"),
        direccion="Sede Demo",
        estado="propuesta",
    )

    proximas = ServicioRecordatorios.comprobar_sesiones_proximas(horas_anticipacion=24)
    assert len(proximas) >= 1
    assert "Sede Demo" in proximas[0]["direccion"]


def test_avisar_proximos_eventos(tmp_path):
    c_id = ContratacionRepository.crear(
        id_cliente=1,
        id_formacion_base=1,
        expediente="EXP-002",
        precio_hora=40,
        horas_previstas=8,
        modalidad="presencial"
    )

    InteraccionRepository.crear(
        id_cliente=1,
        fecha="2025-10-10",
        tipo="reunion",
        descripcion="Revisión propuesta",
        resultado="propuesta",
        proxima_accion="Llamar confirmación",
        fecha_proxima_accion=(datetime.now() + timedelta(hours=12)).strftime("%Y-%m-%d"),
        crear_recordatorio=True,
    )

    # Usar estado permitido por el esquema: "programada"
    SesionRepository.crear(
        id_contratacion=c_id,
        fecha=(datetime.now() + timedelta(hours=18)).strftime("%Y-%m-%d"),
        hora_inicio=(datetime.now() + timedelta(hours=18)).strftime("%H:%M"),
        hora_fin=(datetime.now() + timedelta(hours=20)).strftime("%H:%M"),
        direccion="Oficina Central",
        estado="programada",
    )

    avisos = ServicioRecordatorios.avisar_proximos_eventos()

    assert "recordatorios_interacciones" in avisos
    assert "sesiones_proximas" in avisos
    assert len(avisos["recordatorios_interacciones"]) >= 1
    assert len(avisos["sesiones_proximas"]) >= 1
