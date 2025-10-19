import logging
from datetime import datetime, timedelta
from planificador.data.repositories.interaccion_repo import InteraccionRepository
from planificador.data.repositories.sesion_repo import SesionRepository

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ServicioRecordatorios:
    """
    Servicio para generar recordatorios automáticos a partir de interacciones
    y comprobar avisos próximos en sesiones y contactos comerciales.
    """

    @staticmethod
    def generar_desde_interacciones():
        """
        Revisa interacciones con crear_recordatorio=True y fecha_proxima_accion futura.
        Devuelve lista de recordatorios creados.
        """
        interacciones = InteraccionRepository.listar_todas()
        recordatorios = []

        for inter in interacciones:
            if (
                inter["crear_recordatorio"]
                and inter["fecha_proxima_accion"]
                and datetime.strptime(inter["fecha_proxima_accion"], "%Y-%m-%d").date() >= datetime.now().date()):
                recordatorio = {
                    "tipo": inter["tipo"],
                    "cliente": inter["id_cliente"],
                    "fecha": inter["fecha_proxima_accion"],
                    "descripcion": inter["proxima_accion"] or inter["descripcion"],
                }
                recordatorios.append(recordatorio)
                logger.info(f"Recordatorio generado desde interacción {inter['id_interaccion']}: {recordatorio}")

        logger.info(f"Total recordatorios generados: {len(recordatorios)}")
        return recordatorios

    @staticmethod
    def comprobar_sesiones_proximas(horas_anticipacion=24):
        """
        Devuelve lista de sesiones próximas en el rango de anticipación definido (en horas).
        """
        sesiones = SesionRepository.listar_todas()
        ahora = datetime.now()
        margen = ahora + timedelta(hours=horas_anticipacion)

        proximas = [
            s
            for s in sesiones
            if datetime.strptime(s["fecha"] + " " + s["hora_inicio"], "%Y-%m-%d %H:%M") <= margen
            and datetime.strptime(s["fecha"] + " " + s["hora_inicio"], "%Y-%m-%d %H:%M") >= ahora
        ]

        logger.info(f"Sesiones próximas en las próximas {horas_anticipacion}h: {len(proximas)}")
        return proximas

    @staticmethod
    def avisar_proximos_eventos():
        """
        Genera una lista combinada de avisos por interacciones y sesiones próximas.
        """
        recordatorios = ServicioRecordatorios.generar_desde_interacciones()
        sesiones = ServicioRecordatorios.comprobar_sesiones_proximas()

        avisos = {
            "recordatorios_interacciones": recordatorios,
            "sesiones_proximas": sesiones,
        }

        logger.info(f"Avisos combinados generados: {avisos}")
        return avisos
