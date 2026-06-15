from django.db import models
from apps.clientes.models import Cliente
from seguridad.validadores import validar_identificador_direccion, validar_codigo_postal

class Direccion(models.Model):
    TIPO_CHOICES = [
        ("origen", "Origen"),
        ("destino", "Destino"),
        ("resguardo", "Resguardo"),
        ("otra", "Otra"),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="direcciones"
    )
    identificador = models.CharField(max_length=30, unique=True, validators=[validar_identificador_direccion])
    calle = models.CharField(max_length=150)
    numero = models.CharField(max_length=20)
    colonia = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10, validators=[validar_codigo_postal])
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.identificador} - {self.calle} {self.numero}"
