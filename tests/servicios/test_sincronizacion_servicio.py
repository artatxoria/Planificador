from pathlib import Path
from planificador.servicios.sincronizacion_servicio import ServicioSincronizacion

def test_exportar_a_google_calendar(tmp_path):
    sesiones = [
        {"titulo": "Sesión A", "fecha": "2025-10-10", "hora_inicio": "09:00", "hora_fin": "11:00"},
        {"titulo": "Sesión B", "fecha": "2025-10-11", "hora_inicio": "10:00", "hora_fin": "12:00"}
    ]
    resultado = ServicioSincronizacion.exportar_a_google_calendar(sesiones)
    assert resultado == 2

def test_importar_desde_google_calendar(tmp_path):
    eventos = ServicioSincronizacion.importar_desde_google_calendar()
    assert isinstance(eventos, list)
    assert len(eventos) == 2
    assert "titulo" in eventos[0]

def test_verificar_credenciales():
    assert ServicioSincronizacion.verificar_credenciales() is True
