from django.urls import path
from . import views

app_name = "camiones"

urlpatterns = [
    path("nuevo/", views.crear_camion, name="crear_camion"),
    path("<int:pk>/editar/", views.editar_camion, name="editar_camion"),
]