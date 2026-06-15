from django.apps import AppConfig


class BienesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.bienes"
class CamionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.camiones'
    verbose_name = 'Gestión de Camiones'
