import re
from datetime import date
from django.core.exceptions import ValidationError

PATRON_ID_BIEN = re.compile(r"^b-\d{4}-\d{4}$")
PATRON_ID_DIRECCION = re.compile(r"^d-\d{4}-\d{4}$")
PATRON_CP = re.compile(r"^\d{5}$")
PATRON_PLACA = re.compile(r"^[A-Z0-9-]{6,10}$")

def validar_identificador_bien(valor):
    if not PATRON_ID_BIEN.match(valor):
        raise ValidationError("El identificador debe tener el formato b-XXXX-año.")
    
    anio = int(valor.split("-")[2])
    anio_actual = date.today().year
    
    if anio < 2000 or anio > anio_actual:
        raise ValidationError(f"El año debe estar entre 2000 y {anio_actual}.")

def validar_identificador_direccion(valor):
    if not PATRON_ID_DIRECCION.match(valor):
        raise ValidationError("El identificador de dirección debe tener el formato d-XXXX-año.")
    
    anio = int(valor.split("-")[2])
    anio_actual = date.today().year
    
    if anio < 2000 or anio > anio_actual:
        raise ValidationError(f"El año debe estar entre 2000 y {anio_actual}.")

def validar_codigo_postal(valor):
    if not PATRON_CP.match(valor):
        raise ValidationError("El código postal debe contener exactamente 5 dígitos.")

def validar_placa(valor):
    if not PATRON_PLACA.match(valor.upper()):
        raise ValidationError("La placa debe tener entre 6 y 10 caracteres alfanuméricos.")

def validar_anio_camion(valor):
    anio_actual = date.today().year
    if valor < 1950 or valor > anio_actual + 1:
        raise ValidationError(f"El año del camión debe estar entre 1950 y {anio_actual + 1}.")

def validar_positivo(valor):
    if valor < 0:
        raise ValidationError("Este valor no puede ser negativo.")
