# tests/test_participante_repo.py (Versión corregida probable)

import pytest
from planificador.data.repositories.participante_repo import ParticipanteRepository
from planificador.data.db_manager import get_connection

# --- Funciones auxiliares para gestionar datos de prueba ---

def crear_cliente_final_de_prueba():
    """Inserta un ClienteFinal para las pruebas y devuelve su ID."""
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO ClienteFinal (empresa) VALUES (?)", 
            ("Empresa de Prueba para Participantes",)
        )
        conn.commit()
        return cur.lastrowid

def limpiar_tablas():
    """Limpia las tablas implicadas en los tests."""
    with get_connection() as conn:
        conn.execute("DELETE FROM Participante")
        conn.execute("DELETE FROM ClienteFinal")
        conn.commit()

@pytest.fixture(autouse=True)
def setup_db():
    """Fixture que se ejecuta automáticamente para cada test."""
    limpiar_tablas()
    yield
    limpiar_tablas()

# --- Tests corregidos ---

def test_crear_y_listar_participante():
    # 1. Crear el ClienteFinal necesario
    id_cliente_final_test = crear_cliente_final_de_prueba()

    # 2. Usar el ID válido para crear el Participante
    pid = ParticipanteRepository.crear(
        id_cliente_final=id_cliente_final_test, 
        nombre="Carlos Pérez", 
        telefono="611222333", 
        email="carlos@demo.com"
    )
    assert pid is not None

    # 3. Verificar que el participante se ha creado correctamente
    lista = ParticipanteRepository.listar_por_cliente_final(id_cliente_final_test)
    assert any(p["nombre"] == "Carlos Pérez" for p in lista)

def test_actualizar_participante():
    # 1. Crear el ClienteFinal necesario
    id_cliente_final_test = crear_cliente_final_de_prueba()

    # 2. Crear un participante de prueba usando el ID válido
    pid = ParticipanteRepository.crear(id_cliente_final=id_cliente_final_test, nombre="Marta")
    
    # 3. Actualizar los datos del participante
    ParticipanteRepository.actualizar(pid, email="marta@nuevo.com", observaciones="Asistencia confirmada")
    
    # 4. Obtener y verificar los datos actualizados
    datos = ParticipanteRepository.obtener_por_id(pid)
    assert datos is not None
    assert datos["email"] == "marta@nuevo.com"
    assert datos["observaciones"] == "Asistencia confirmada"

