import pytest
from planificador.data.db_manager import init_db
from planificador.data.repositories.cliente_repo import ClienteRepository
from planificador.data.repositories.tema_repo import TemaRepository
from planificador.data.repositories.formacion_base_repo import FormacionBaseRepository
from planificador.data.repositories.contratacion_repo import ContratacionRepository
from planificador.servicios.servicio_calendario import crear_sesion_validada

@pytest.fixture(autouse=True)
def setup_db():
    init_db(force=True)

def _preparar_contratacion_basica():
    cli_id = ClienteRepository.crear("Empresa Demo", "B12345678")
    tema_id = TemaRepository.crear("Ofimática")
    fb_id = FormacionBaseRepository.crear("Excel Básico", tema_id)
    c_id = ContratacionRepository.crear(cli_id, fb_id, expediente="EXP-TEST")
    return c_id

def test_prohibe_solape():
    c_id = _preparar_contratacion_basica()
    # Sesión 09:00-12:00
    crear_sesion_validada(c_id, "2025-10-01", "09:00", "12:00", direccion="Sede A")
    # Intento de solape 11:00-13:00
    with pytest.raises(ValueError) as e:
        crear_sesion_validada(c_id, "2025-10-01", "11:00", "13:00", direccion="Sede A")
    assert "Solape" in str(e.value)

def test_avisa_margen_insuficiente_si_direcciones_distintas():
    c_id = _preparar_contratacion_basica()
    # Sesión 09:00-12:00 en Sede A
    crear_sesion_validada(c_id, "2025-10-02", "09:00", "12:00", direccion="Sede A")
    # Nueva sesión 12:30-14:00 en Sede B -> margen 30' < 60' (por defecto), debe avisar
    with pytest.raises(ValueError) as e:
        crear_sesion_validada(c_id, "2025-10-02", "12:30", "14:00", direccion="Sede B")
    assert "Margen insuficiente" in str(e.value)

def test_permite_margen_insuficiente_si_se_autoriza():
    c_id = _preparar_contratacion_basica()
    # 09:00-12:00 en Sede A
    crear_sesion_validada(c_id, "2025-10-03", "09:00", "12:00", direccion="Sede A")
    # 12:30-14:00 en Sede B -> se permite con flag y devuelve avisos
    res = crear_sesion_validada(c_id, "2025-10-03", "12:30", "14:00", direccion="Sede B",
                                permitir_margen_insuficiente=True)
    assert res["id_sesion"] > 0
    assert any("Margen insuficiente" in a for a in res["avisos"])

def test_no_avisa_si_mismo_lugar_o_online():
    c_id = _preparar_contratacion_basica()
    # 09:00-12:00 online
    crear_sesion_validada(c_id, "2025-10-04", "09:00", "12:00", direccion="online")
    # 12:15-14:00 online (margen 15' pero mismo lugar normalizado -> sin aviso)
    res = crear_sesion_validada(c_id, "2025-10-04", "12:15", "14:00", direccion="videoconferencia",
                                permitir_margen_insuficiente=False)
    assert res["id_sesion"] > 0
    assert res["avisos"] == []
