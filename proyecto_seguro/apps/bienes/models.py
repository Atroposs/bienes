from django.db import models
from apps.clientes.models import Cliente

class Bien(models.Model):
    ESTATUS_CHOICES = [
        ("bueno", "Bueno"),
        ("regular", "Regular"),
        ("malo", "Malo"),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="bienes",
        null=True, # Added null=True to avoid migration issues with existing data
    )
    identificador = models.CharField(max_length=30, unique=True)
    descripcion = models.TextField()
    marca = models.CharField(max_length=80)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.identificador
