import pytest
from planificador.data.repositories.contacto_cliente_final_repo import ContactoClienteFinalRepository
from planificador.data.db_manager import get_connection

# Función auxiliar para crear un ClienteFinal y obtener su ID
def crear_cliente_final_de_prueba():
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO ClienteFinal (empresa) VALUES (?)", 
            ("Empresa de Prueba",)
        )
        conn.commit()
        return cur.lastrowid

def limpiar_tablas():
    with get_connection() as conn:
        # Es importante limpiar ambas tablas para evitar conflictos
        conn.execute("DELETE FROM ContactoClienteFinal")
        conn.execute("DELETE FROM ClienteFinal")
        conn.commit()

@pytest.fixture(autouse=True)
def setup_db():
    limpiar_tablas()
    yield
    limpiar_tablas()

def test_crear_y_listar_contactos():
    # 1. Crear un ClienteFinal para poder asociar el contacto
    id_cliente_final_test = crear_cliente_final_de_prueba()

    # 2. Ahora sí, crear el contacto usando el ID del cliente final válido
    nuevo_id = ContactoClienteFinalRepository.crear(
        id_cliente_final=id_cliente_final_test,
        nombre="Laura Ruiz", 
        telefono="600999888", 
        email="laura@x.com", 
        rol="encargado_formacion"
    )
    assert nuevo_id is not None

    # 3. La aserción de la lista debería funcionar como antes
    lista = ContactoClienteFinalRepository.listar_por_cliente_final(id_cliente_final_test)
    assert any(c["nombre"] == "Laura Ruiz" for c in lista)

def test_actualizar_contacto():
    # 1. Crear un ClienteFinal de prueba
    id_cliente_final_test = crear_cliente_final_de_prueba()

    # 2. Crear el contacto, asegurándose de pasar el id_cliente_final requerido
    id_contacto = ContactoClienteFinalRepository.crear(
        id_cliente_final=id_cliente_final_test, 
        nombre="Pedro", 
        rol="otro"
    )
    
    # 3. Actualizar el contacto
    ContactoClienteFinalRepository.actualizar(id_contacto, telefono="600000000", rol="participante")
    
    # 4. Verificar los datos actualizados
    datos = ContactoClienteFinalRepository.obtener_por_id(id_contacto)
    assert datos["telefono"] == "600000000"
    assert datos["rol"] == "participante"