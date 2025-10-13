import pytest
from pathlib import Path
from planificador.data.db_manager import init_db, get_connection
from planificador.servicios.exportacion_servicio import ServicioExportacion

@pytest.fixture(autouse=True)
def setup_db(tmp_path):
    init_db(force=True)
    with get_connection() as conn:
        conn.execute("INSERT INTO Cliente (empresa, cif) VALUES ('Demo SA', 'B00000000')")
        conn.commit()
    yield

def test_exportar_csv(tmp_path):
    ruta = tmp_path / "clientes.csv"
    resultado = ServicioExportacion.exportar_csv("Cliente", ruta)
    assert resultado.exists()
    contenido = ruta.read_text(encoding="utf-8")
    assert "empresa" in contenido
    assert "Demo SA" in contenido
