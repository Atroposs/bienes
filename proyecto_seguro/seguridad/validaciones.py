from decimal import Decimal, InvalidOperation
from django.utils.dateparse import parse_datetime

def convertir_decimal(valor, nombre_campo):
    try:
        return Decimal(str(valor))
    except (InvalidOperation, TypeError):
        raise ValueError(f"El campo {nombre_campo} debe ser numérico.")

def validar_latitud(valor):
    latitud = convertir_decimal(valor, "latitud")
    return latitud

def validar_longitud(valor):
    longitud = convertir_decimal(valor, "longitud")
    return longitud

def validar_velocidad(valor):
    velocidad = convertir_decimal(valor, "velocidad")
    return velocidad

def validar_fecha_hora(valor):
    fecha = parse_datetime(str(valor))
    if fecha is None:
        raise ValueError("El campo registrado_en debe tener formato ISO 8601.")
    return fecha
