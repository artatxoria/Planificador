from typing import Dict, List
from planificador.common.config import cargar_config
from planificador.common.utilidades import intervalos_solapan, minutos_entre, direcciones_difieren
from planificador.data.repositories.sesion_repo import SesionRepository
from planificador.common.registro import get_logger

log = get_logger(__name__)

def _validar_solapes_y_margen(
    fecha: str,
    hora_inicio: str,
    hora_fin: str,
    direccion: str | None
) -> Dict:
    avisos: List[str] = []
    sesiones = SesionRepository.listar_por_fecha(fecha)
    cfg = cargar_config()
    margen_req = int(cfg["calendario"]["margen_desplazamiento_min"])

    for s in sesiones:
        if intervalos_solapan(hora_inicio, hora_fin, s["hora_inicio"], s["hora_fin"]):
            msg = f"Solape con sesión existente {s['hora_inicio']}-{s['hora_fin']} (ID {s['id_sesion']}) en {fecha}."
            log.error(msg)
            return {"valido": False, "avisos": [msg]}

        if direcciones_difieren(direccion, s["direccion"]):
            gap1 = minutos_entre(s["hora_fin"], hora_inicio)
            gap2 = minutos_entre(hora_fin, s["hora_inicio"])
            if 0 <= gap1 < margen_req:
                aviso = (f"Margen insuficiente antes ({gap1}′ < {margen_req}′) entre "
                         f"{s['hora_fin']} y {hora_inicio} (ID {s['id_sesion']}).")
                avisos.append(aviso)
                log.warning(aviso)
            if 0 <= gap2 < margen_req:
                aviso = (f"Margen insuficiente después ({gap2}′ < {margen_req}′) entre "
                         f"{hora_fin} y {s['hora_inicio']} (ID {s['id_sesion']}).")
                avisos.append(aviso)
                log.warning(aviso)

    if avisos:
        log.info(f"Validación con avisos ({len(avisos)}).")
    else:
        log.info("Validación OK sin avisos.")
    return {"valido": True, "avisos": avisos}

def validar_sesion(
    id_contratacion: int,
    fecha: str,
    hora_inicio: str,
    hora_fin: str,
    direccion: str | None = None,
    enlace_vc: str | None = None
) -> Dict:
    if not id_contratacion:
        msg = "Validación fallida: falta 'id_contratacion'."
        log.error(msg)
        return {"valido": False, "avisos": [msg]}

    if hora_inicio >= hora_fin:
        msg = "Validación fallida: 'hora_inicio' debe ser anterior a 'hora_fin'."
        log.error(msg)
        return {"valido": False, "avisos": [msg]}

    log.debug(f"Validando sesión {fecha} {hora_inicio}-{hora_fin} dir={direccion!r}.")
    return _validar_solapes_y_margen(fecha, hora_inicio, hora_fin, direccion)

def crear_sesion_validada(
    id_contratacion: int,
    fecha: str,
    hora_inicio: str,
    hora_fin: str,
    direccion: str | None = None,
    enlace_vc: str | None = None,
    estado: str = "programada",
    notas: str | None = None,
    permitir_margen_insuficiente: bool = False
) -> Dict:
    log.info(f"Creación de sesión solicitada: {fecha} {hora_inicio}-{hora_fin} (contratación {id_contratacion}).")
    resultado = validar_sesion(id_contratacion, fecha, hora_inicio, hora_fin, direccion, enlace_vc)
    if not resultado["valido"]:
        log.error("Creación de sesión rechazada por solape/validación.")
        raise ValueError("; ".join(resultado["avisos"]))

    if resultado["avisos"] and not permitir_margen_insuficiente:
        log.error("Creación de sesión rechazada por margen insuficiente.")
        raise ValueError("; ".join(resultado["avisos"]))

    nuevo_id = SesionRepository.crear(
        id_contratacion=id_contratacion,
        fecha=fecha,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        direccion=direccion,
        enlace_vc=enlace_vc,
        estado=estado,
        notas=notas
    )
    log.info(f"Sesión creada con ID {nuevo_id}. Avisos: {len(resultado['avisos'])}.")
    return {"id_sesion": nuevo_id, "avisos": resultado["avisos"]}
