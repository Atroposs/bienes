from django.db import models
from django.contrib.auth.models import User

class Empleado(models.Model):
    PUESTO_CHOICES = [
        ("encargado", "Encargado"),
    ]

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="empleado",
        null=True,
        blank=True
    )
    
    identificador = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=120)
    apellido_paterno = models.CharField(max_length=120)
    apellido_materno = models.CharField(max_length=120)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    puesto = models.CharField(max_length=30, choices=PUESTO_CHOICES, default="encargado")
    fecha_ingreso = models.DateField()
    activo = models.BooleanField(default=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"

    def __str__(self):
        return f"{self.identificador} - {self.nombre_completo}"

class UbicacionEmpleado(models.Model):
    empleado = models.ForeignKey(
        Empleado, 
        on_delete=models.CASCADE, 
        related_name="ubicaciones"
    )
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    registrado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-registrado_en']

    def __str__(self):
        return f"{self.empleado.identificador} - {self.latitud}, {self.longitud}"
