from django.urls import path
from . import views

app_name = "direcciones"

urlpatterns = [
    path("nueva/", views.crear_direccion, name="crear_direccion"),
    path("mis-direcciones/", views.reporte_mis_direcciones, name="reporte_mis_direcciones"),
    path("editar/<int:pk>/", views.editar_direccion, name="editar_direccion"),
]
