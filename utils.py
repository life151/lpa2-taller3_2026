import re
from datetime import datetime


def validar_correo(correo: str) -> bool:
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(patron, correo))


def formatear_duracion(segundos: int) -> str:
    return f"{segundos // 60:02d}:{segundos % 60:02d}"


def generar_slug(texto: str) -> str:
    slug = texto.lower().replace(" ", "-")
    slug = re.sub(r"[^a-z0-9áéíóúñ-]", "", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def obtener_año_actual() -> int:
    return datetime.now().year


def validar_año(año: int) -> bool:
    return 1900 <= año <= obtener_año_actual()
