import pytest
from planificador.data.db_manager import init_db
from planificador.data.repositories.cliente_repo import ClienteRepository
from planificador.data.repositories.tema_repo import TemaRepository
from planificador.data.repositories.formacion_base_repo import FormacionBaseRepository
from planificador.data.repositories.contratacion_repo import ContratacionRepository
from planificador.servicios.servicio_calendario import crear_sesion_validada
from planificador.dominio.modelos.contratacion import Contratacion

@pytest.fixture(autouse=True)
def setup_db():
    init_db(force=True)

def _preparar_contratacion(precio_hora=50, horas_previstas=10):
    cli_id = ClienteRepository.crear("Empresa Test", "B99999999")
    tema_id = TemaRepository.crear("Ofimática")
    fb_id = FormacionBaseRepository.crear("Excel Básico", tema_id)
    c_id = ContratacionRepository.crear(cli_id, fb_id, expediente="EXP-NEGOCIO",
                                        precio_hora=precio_hora, horas_previstas=horas_previstas)
    return c_id

def test_calculo_horas_y_honorarios():
    c_id = _preparar_contratacion(precio_hora=40, horas_previstas=8)

    # Creamos dos sesiones de 2h cada una
    crear_sesion_validada(c_id, "2025-10-10", "09:00", "11:00", direccion="Sede A")
    crear_sesion_validada(c_id, "2025-10-11", "10:00", "12:00", direccion="Sede A")

    # Recuperamos como objeto de dominio
    contrato = Contratacion(id_cliente=1, id_formacion_base=1,
                            expediente="EXP-NEGOCIO", precio_hora=40,
                            horas_previstas=8, id_contratacion=c_id)

    assert contrato.calcular_horas_totales() == 4.0
    assert contrato.calcular_horas_restantes() == 4.0
    assert contrato.calcular_honorarios() == 160.0
