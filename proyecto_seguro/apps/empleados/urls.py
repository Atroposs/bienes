from django.urls import path
from . import views

app_name = "empleados"

urlpatterns = [
    path("panel/", views.panel_encargado, name="panel_encargado"),
    path("api/ubicacion/", views.actualizar_ubicacion, name="actualizar_ubicacion"),
    path("api/ubicaciones/", views.listar_ubicaciones, name="listar_ubicaciones"),
]
