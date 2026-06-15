from django.contrib import admin
from .models import Empleado, UbicacionEmpleado

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("identificador", "nombre", "apellido_paterno", "puesto", "activo")
    search_fields = ("identificador", "nombre", "apellido_paterno")
    list_filter = ("puesto", "activo")

@admin.register(UbicacionEmpleado)
class UbicacionEmpleadoAdmin(admin.ModelAdmin):
    list_display = ("empleado", "latitud", "longitud", "registrado_en")
    list_filter = ("empleado",)
