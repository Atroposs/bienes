from django.urls import path
from . import views

app_name = "bienes"

urlpatterns = [
    # Rutas de bienes
    path("", views.lista_bienes, name="lista_bienes"),
    path("nuevo/", views.crear_bien, name="crear_bien"),
    path("mis-bienes/", views.reporte_mis_bienes, name="reporte_mis_bienes"),
    path("reporte-general/", views.reporte_general_bienes, name="reporte_general_bienes"),
]
