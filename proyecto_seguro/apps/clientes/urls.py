from django.urls import path
from . import views

app_name = "clientes"

urlpatterns = [
    path("registro/", views.registro, name="registro"),
    path("auditor/autorizar/<int:cliente_id>/", views.autorizar_cliente, name="autorizar_cliente"),
]