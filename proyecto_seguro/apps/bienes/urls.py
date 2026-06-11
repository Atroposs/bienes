from django.urls import path
from . import views

app_name = "bienes"

urlpatterns = [
    path("", views.home_router, name="home_router"),
    path("bienes/", views.lista_bienes, name="lista_bienes"),
    path("bienes/nuevo/", views.crear_bien, name="crear_bien"),
    path("bienes/mis-bienes/", views.reporte_mis_bienes, name="reporte_mis_bienes"),
    path("bienes/reporte-general/", views.reporte_general_bienes, name="reporte_general_bienes"),
    path("supervisor/clientes/", views.lista_clientes_supervisor, name="lista_clientes_supervisor"),
    path("supervisor/clientes/autorizar/<int:cliente_id>/", views.autorizar_cliente, name="autorizar_cliente"),
]
