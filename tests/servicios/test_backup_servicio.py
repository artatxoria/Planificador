import shutil   # 🔹 ← Añadido aquí
import pytest
from pathlib import Path
from planificador.servicios.backup_servicio import ServicioBackup
from planificador.data.db_manager import init_db

@pytest.fixture
def setup_db(tmp_path):
    db_path = tmp_path / "planificador.db"
    init_db(force=True)
    origen = Path.cwd() / "planificador.db"
    if origen.exists():
        shutil.copy2(origen, db_path)
    yield db_path

def test_realizar_y_listar_backup(tmp_path, setup_db):
    carpeta_backups = tmp_path / "backups"
    resultado = ServicioBackup.realizar_backup(setup_db, carpeta_backups, max_copias=3)
    assert resultado.exists()

    backups = ServicioBackup.listar_backups(carpeta_backups)
    assert len(backups) == 1
    assert backups[0].name.startswith("planificador_backup_")

def test_restaurar_backup(tmp_path, setup_db):
    carpeta_backups = tmp_path / "backups"
    backup = ServicioBackup.realizar_backup(setup_db, carpeta_backups)
    db_destino = tmp_path / "restaurado.db"
    ok = ServicioBackup.restaurar_backup(backup, db_destino)
    assert ok
    assert db_destino.exists()

