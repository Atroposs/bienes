from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home_router, name="home_router"),
    path("general/", views.panel_control_auditor, name="panel_control_auditor"),
]
