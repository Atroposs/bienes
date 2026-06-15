from django.db import models

class Camion(models.Model):
    TIPO_COMBUSTIBLE_CHOICES = [
        ("diesel", "Diésel"),
        ("gasolina", "Gasolina"),
        ("electrico", "Eléctrico"),
        ("gas", "Gas Natural"),
    ]

    ESTADO_CHOICES = [
        ("disponible", "Disponible"),
        ("mantenimiento", "En Mantenimiento"),
        ("fuera_servicio", "Fuera de Servicio"),
        ("en_ruta", "En Ruta"),
    ]

    placa = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField(verbose_name="año")
    numero_serie = models.CharField(max_length=50, unique=True)
    capacidad_carga_kg = models.DecimalField(max_digits=10, decimal_places=2)
    kilometraje_actual = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_combustible = models.CharField(max_length=20, choices=TIPO_COMBUSTIBLE_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="disponible")
    activo = models.BooleanField(default=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo} ({self.anio})"

    class Meta:
        verbose_name = "camión"
        verbose_name_plural = "camiones"

