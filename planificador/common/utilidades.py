from typing import Optional

def a_minutos(hhmm: str) -> int:
    """Convierte 'HH:MM' a minutos desde medianoche."""
    if not hhmm or len(hhmm) != 5 or hhmm[2] != ":":
        raise ValueError("Formato de hora inválido, se espera 'HH:MM'")
    h = int(hhmm[0:2])
    m = int(hhmm[3:5])
    if h < 0 or h > 23 or m < 0 or m > 59:
        raise ValueError("Hora fuera de rango")
    return h * 60 + m

def intervalos_solapan(inicio1: str, fin1: str, inicio2: str, fin2: str) -> bool:
    """Devuelve True si [inicio1, fin1) se solapa con [inicio2, fin2)."""
    i1, f1 = a_minutos(inicio1), a_minutos(fin1)
    i2, f2 = a_minutos(inicio2), a_minutos(fin2)
    if not (i1 < f1 and i2 < f2):
        raise ValueError("Intervalos no válidos (inicio < fin)")
    return i1 < f2 and i2 < f1

def minutos_entre(fin1: str, inicio2: str) -> int:
    """Minutos entre fin1 y inicio2 (puede ser negativo si se solapan/encadenan)."""
    return a_minutos(inicio2) - a_minutos(fin1)

def normalizar_direccion(texto: Optional[str]) -> str:
    """Normaliza dirección para comparación (maneja 'online'/'remoto')."""
    if not texto:
        return ""
    t = texto.strip().lower()
    if t in {"online", "on-line", "remoto", "videoconferencia", "video", "vc"}:
        return "online"
    return " ".join(t.split())

def direcciones_difieren(dir1: Optional[str], dir2: Optional[str]) -> bool:
    """True si ambas están informadas y no equivalen."""
    n1, n2 = normalizar_direccion(dir1), normalizar_direccion(dir2)
    if not n1 or not n2:
        return False  # si falta alguna, no forzamos diferencia
    return n1 != n2
