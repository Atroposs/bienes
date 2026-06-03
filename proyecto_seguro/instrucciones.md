```markdown
# Guía de Ejecución: Proyecto Logística Django

Este documento contiene las operaciones en orden cronológico para que el agente `antigravity` configure y programe el proyecto logístico en Django.

Antes que nada quiero que notes que alguno de estos cambios ya se realizaron para que no modifiques lo ya hecho y omitas lo que ya se realizo, segundo quiero que recuerdes aplicar estos cambios manteniendo los estilos que ya venimos manejando dentro del proyecto y si tienes alguna duda me preguntes antes de realizar operaciones.
## Fase 1: Inicialización y Autenticación (Versión 1)

### 1. Creación del entorno y proyecto
Ejecutar los siguientes comandos en la terminal:

el entorno ya fue creado se puede omitir

### 2. Configuración de la app `bienes`
Editar **`apps/bienes/apps.py`**:
```python
from django.apps import AppConfig

class BienesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.bienes"
```

### 3. Ajustes globales (`settings.py`)
Editar **`config/settings.py`**. 
Agregar `apps.bienes` a `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.bienes",
]
```
Actualizar `TEMPLATES` añadiendo la ruta del directorio base:
```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
```
Agregar al final de **`config/settings.py`**:
```python
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "bienes:lista"
LOGOUT_REDIRECT_URL = "login"
```

### 4. Rutas Iniciales y Vistas
Crear **`apps/bienes/urls.py`**:
```python
from django.urls import path
from . import views

app_name = "bienes"

urlpatterns = [
    path("", views.lista_bienes, name="lista"),
    path("nuevo/", views.crear_bien, name="crear"),
]
```
Editar **`config/urls.py`**:
```python
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path("bienes/", include("apps.bienes.urls")),
]
```

### 5. Creación de directorios para plantillas
```bash
mkdir templates
mkdir templates/registration
mkdir -p apps/bienes/templates/bienes
```

### 6. Archivos HTML (Versión 1)
Crear **`templates/base.html`**:
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Proyecto seguro{% endblock %}</title>
</head>
<body>
    <header>
        <h1>Proyecto seguro en Django</h1>
        {% if user.is_authenticated %}
            <p>Usuario: {{ user.username }}</p>
            <form method="post" action="{% url 'logout' %}">
                {% csrf_token %}
                <button type="submit">Cerrar sesión</button>
            </form>
        {% endif %}
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```
Crear **`templates/registration/login.html`**:
```html
{% extends "base.html" %}

{% block title %}Iniciar sesión{% endblock %}

{% block content %}
<h2>Iniciar sesión</h2>
{% if form.errors %}
    <p>Usuario o contraseña inválidos.</p>
{% endif %}

<form method="post">
    {% csrf_token %}
    <p>
        <label for="{{ form.username.id_for_label }}">Usuario</label><br>
        {{ form.username }}
    </p>
    <p>
        <label for="{{ form.password.id_for_label }}">Contraseña</label><br>
        {{ form.password }}
    </p>
    <button type="submit">Entrar</button>
</form>
{% endblock %}
```

---

## Fase 2: Modelos y Formularios (Versión 2)

### 1. Crear el modelo Bien
Editar **`apps/bienes/models.py`**:
```python
from django.db import models

class Bien(models.Model):
    ESTATUS_CHOICES = [
        ("bueno", "Bueno"),
        ("regular", "Regular"),
        ("malo", "Malo"),
    ]

    identificador = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=150)
    marca = models.CharField(max_length=80)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    estatus = models.CharField(max_length=10, choices=ESTATUS_CHOICES)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.identificador
```

### 2. Generar y aplicar migraciones iniciales
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Crear el formulario
Crear **`apps/bienes/forms.py`**:
```python
from django import forms
from .models import Bien

class BienForm(forms.ModelForm):
    class Meta:
        model = Bien
        fields = [
            "identificador",
            "descripcion",
            "marca",
            "valor",
            "estatus",
        ]
```

### 4. Actualizar las vistas de bienes
Editar **`apps/bienes/views.py`**:
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import BienForm
from .models import Bien

@login_required
def lista_bienes(request):
    bienes = Bien.objects.all().order_by("identificador")
    return render(request, "bienes/lista.html", {"bienes": bienes})

@login_required
def crear_bien(request):
    if request.method == "POST":
        form = BienForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("bienes:lista")
    else:
        form = BienForm()
    return render(request, "bienes/formulario.html", {"form": form})
```

### 5. Actualizar Templates de Bienes
Editar **`apps/bienes/templates/bienes/lista.html`**:
```html
{% extends "base.html" %}
{% block title %}Bienes registrados{% endblock %}

{% block content %}
<h2>Bienes registrados</h2>
<p>
    <a href="{% url 'bienes:crear' %}">Registrar nuevo bien</a>
</p>
<table border="1">
    <thead>
        <tr>
            <th>Identificador</th>
            <th>Descripción</th>
            <th>Marca</th>
            <th>Valor</th>
            <th>Estatus</th>
        </tr>
    </thead>
    <tbody>
        {% for bien in bienes %}
            <tr>
                <td>{{ bien.identificador }}</td>
                <td>{{ bien.descripcion }}</td>
                <td>{{ bien.marca }}</td>
                <td>{{ bien.valor }}</td>
                <td>{{ bien.estatus }}</td>
            </tr>
        {% empty %}
            <tr>
                <td colspan="5">No hay bienes registrados.</td>
            </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```
Editar **`apps/bienes/templates/bienes/formulario.html`**:
```html
{% extends "base.html" %}
{% block title %}Registrar bien{% endblock %}

{% block content %}
<h2>Registrar bien</h2>
<form method="post">
    {% csrf_token %}
    {{ form.non_field_errors }}
    
    {% for field in form %}
        <p>
            {{ field.label_tag }}<br>
            {{ field }}
            {% if field.errors %}
                <br>
                <strong>{{ field.errors }}</strong>
            {% endif %}
        </p>
    {% endfor %}
    <button type="submit">Guardar</button>
</form>
<p>
    <a href="{% url 'bienes:lista' %}">Volver al listado</a>
</p>
{% endblock %}
```

---

## Fase 3: Capa de Seguridad y Validaciones (Versión 3)

### 1. Crear el paquete `seguridad`
Ejecutar en la raíz:
```bash
mkdir seguridad
touch seguridad/__init__.py
touch seguridad/validadores.py
```

### 2. Implementar validador de identificador
Editar **`seguridad/validadores.py`**:
```python
import re
from datetime import date
from django.core.exceptions import ValidationError

PATRON_ID_BIEN = re.compile(r"^b-\d{4}-\d{4}$")

def validar_identificador_bien(valor):
    if not PATRON_ID_BIEN.match(valor):
        raise ValidationError("El identificador debe tener el formato b-XXXX-año.")
    
    anio = int(valor.split("-"))
    anio_actual = date.today().year
    
    if anio < 2000 or anio > anio_actual:
        raise ValidationError(f"El año debe estar entre 2000 y {anio_actual}.")
```

### 3. Conectar el validador al formulario
Editar **`apps/bienes/forms.py`**:
```python
from django import forms
from .models import Bien
from seguridad.validadores import validar_identificador_bien

class BienForm(forms.ModelForm):
    class Meta:
        model = Bien
        fields = [
            "identificador",
            "descripcion",
            "marca",
            "valor",
            "estatus",
        ]

    def clean_identificador(self):
        identificador = self.cleaned_data["identificador"].strip()
        validar_identificador_bien(identificador)
        return identificador
```

---

## Fase 4: Autorización y Roles

### 1. Crear la app Clientes
```bash
python manage.py startapp clientes apps/clientes
```
Editar **`apps/clientes/apps.py`**:
```python
from django.apps import AppConfig

class ClientesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.clientes"
```
Añadir `"apps.clientes"` a la lista de `INSTALLED_APPS` en **`config/settings.py`**.

### 2. Modelo Cliente y Administrador
Editar **`apps/clientes/models.py`**:
```python
from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cliente"
    )
    identificador = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=120)
    apellido_paterno = models.CharField(max_length=120)
    apellido_materno = models.CharField(max_length=120)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"

    def __str__(self):
        return self.identificador
```
Editar **`apps/clientes/admin.py`**:
```python
from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "identificador",
        "nombre",
        "apellido_paterno",
        "apellido_materno",
        "correo",
        "telefono",
        "usuario",
        "creado_en",
        "actualizado_en",
    )
    search_fields = (
        "identificador",
        "nombre",
        "apellido_paterno",
        "apellido_materno",
        "correo",
    )
```

### 3. Actualizar la relación del Bien
Editar **`apps/bienes/models.py`**:
```python
from django.db import models
from apps.clientes.models import Cliente

class Bien(models.Model):
    ESTATUS_CHOICES = [
        ("bueno", "Bueno"),
        ("regular", "Regular"),
        ("malo", "Malo"),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="bienes"
    )
    identificador = models.CharField(max_length=30, unique=True)
    descripcion = models.TextField()
    marca = models.CharField(max_length=80)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.identificador
```
Generar y aplicar migraciones:
```bash
python manage.py makemigrations clientes
python manage.py makemigrations bienes
python manage.py migrate
```

### 4. Lógica de Roles y Decoradores
Crear **`seguridad/roles.py`**:
```python
GRUPO_CLIENTE = "cliente"
GRUPO_SUPERVISOR = "supervisor"

def pertenece_a_grupo(user, nombre_grupo):
    return user.is_authenticated and user.groups.filter(name=nombre_grupo).exists()

def es_cliente(user):
    return pertenece_a_grupo(user, GRUPO_CLIENTE)

def es_supervisor(user):
    return pertenece_a_grupo(user, GRUPO_SUPERVISOR)
```
Crear **`seguridad/decorators.py`**:
```python
from functools import wraps
from django.core.exceptions import PermissionDenied
from .roles import es_cliente, es_supervisor

def supervisor_requerido(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not es_supervisor(request.user):
            raise PermissionDenied("Se requiere rol de supervisor.")
        return view_func(request, *args, **kwargs)
    return wrapper

def cliente_requerido(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not es_cliente(request.user):
            raise PermissionDenied("Se requiere rol de cliente.")
        return view_func(request, *args, **kwargs)
    return wrapper
```

### 5. Actualizar vistas protegidas
Reescribir completamente **`apps/bienes/views.py`** con protección y reportes:
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from seguridad.decorators import cliente_requerido, supervisor_requerido
from seguridad.roles import es_cliente, es_supervisor
from .forms import BienForm
from .models import Bien

@login_required
@cliente_requerido
def crear_bien(request):
    cliente = request.user.cliente
    if request.method == "POST":
        form = BienForm(request.POST)
        if form.is_valid():
            bien = form.save(commit=False)
            bien.cliente = cliente
            bien.save()
            return redirect("reporte_mis_bienes")
    else:
        form = BienForm()
    return render(request, "bienes/crear_bien.html", {"form": form})

@login_required
@cliente_requerido
def reporte_mis_bienes(request):
    bienes = Bien.objects.filter(cliente__usuario=request.user).order_by("-creado_en")
    return render(request, "bienes/reporte_mis_bienes.html", {"bienes": bienes})

@login_required
@supervisor_requerido
def reporte_general_bienes(request):
    bienes = Bien.objects.select_related("cliente").order_by("-creado_en")
    return render(request, "bienes/reporte_general_bienes.html", {"bienes": bienes})

@login_required
def lista_bienes(request):
    if es_supervisor(request.user):
        bienes = Bien.objects.select_related("cliente").all()
    elif es_cliente(request.user):
        bienes = Bien.objects.filter(cliente__usuario=request.user)
    else:
        bienes = Bien.objects.none()

    return render(
        request,
        "bienes/lista_bienes.html",
        {
            "bienes": bienes,
            "es_cliente": es_cliente(request.user),
            "es_supervisor": es_supervisor(request.user),
        }
    )
```

Actualizar **`apps/bienes/urls.py`**:
```python
from django.urls import path
from . import views

urlpatterns = [
    path("bienes/", views.lista_bienes, name="lista_bienes"),
    path("bienes/nuevo/", views.crear_bien, name="crear_bien"),
    path("bienes/mis-bienes/", views.reporte_mis_bienes, name="reporte_mis_bienes"),
    path("bienes/reporte-general/", views.reporte_general_bienes, name="reporte_general_bienes"),
]
```

### 6. Templates para Autorización
Reemplazar/Crear los templates en `apps/bienes/templates/bienes/`:

**`crear_bien.html`**
```html
<h1>Registrar bien</h1>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Guardar</button>
</form>
<a href="{% url 'reporte_mis_bienes' %}">Ver mis bienes</a>
```

**`reporte_mis_bienes.html`**
```html
<h1>Mis bienes registrados</h1>
<a href="{% url 'crear_bien' %}">Registrar nuevo bien</a>
<table>
  <thead>
    <tr>
      <th>Identificador</th><th>Descripción</th><th>Marca</th><th>Valor</th><th>Estatus</th>
    </tr>
  </thead>
  <tbody>
    {% for bien in bienes %}
      <tr>
        <td>{{ bien.identificador }}</td><td>{{ bien.descripcion }}</td><td>{{ bien.marca }}</td><td>{{ bien.valor }}</td><td>{{ bien.estatus }}</td>
      </tr>
    {% empty %}
      <tr><td colspan="5">No hay bienes registrados.</td></tr>
    {% endfor %}
  </tbody>
</table>
```

**`reporte_general_bienes.html`**
```html
<h1>Reporte general de bienes</h1>
<table>
  <thead>
    <tr>
      <th>Cliente</th><th>Identificador</th><th>Descripción</th><th>Marca</th><th>Valor</th><th>Estatus</th>
    </tr>
  </thead>
  <tbody>
    {% for bien in bienes %}
      <tr>
        <td>{{ bien.cliente.nombre_completo }}</td><td>{{ bien.identificador }}</td><td>{{ bien.descripcion }}</td><td>{{ bien.marca }}</td><td>{{ bien.valor }}</td><td>{{ bien.estatus }}</td>
      </tr>
    {% empty %}
      <tr><td colspan="6">No hay bienes registrados.</td></tr>
    {% endfor %}
  </tbody>
</table>
```

**`lista_bienes.html`**
```html
<h1>Bienes</h1>
{% if es_cliente %}
  <a href="{% url 'crear_bien' %}">Registrar bien</a>
  <a href="{% url 'reporte_mis_bienes' %}">Mis bienes</a>
{% endif %}
{% if es_supervisor %}
  <a href="{% url 'reporte_general_bienes' %}">Reporte general</a>
{% endif %}
<table>
  <thead>
    <tr>
      <th>Identificador</th><th>Descripción</th><th>Marca</th><th>Valor</th><th>Estatus</th>
    </tr>
  </thead>
  <tbody>
    {% for bien in bienes %}
      <tr>
        <td>{{ bien.identificador }}</td><td>{{ bien.descripcion }}</td><td>{{ bien.marca }}</td><td>{{ bien.valor }}</td><td>{{ bien.estatus }}</td>
      </tr>
    {% empty %}
      <tr><td colspan="5">No hay bienes registrados.</td></tr>
    {% endfor %}
  </tbody>
</table>
```

---

## Fase 5: Servicios REST y Rastreo

### 1. Crear app Rastreo
```bash
python manage.py startapp rastreo apps/rastreo
```
Editar **`apps/rastreo/apps.py`**:
```python
from django.apps import AppConfig

class RastreoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.rastreo"
```
Añadir `"apps.rastreo"` a `INSTALLED_APPS` en **`config/settings.py`** y configurar el Token al final del archivo:
```python
TOKEN_RASTREO_CAMIONES = "TOKEN_DE_PRACTICA_CAMIONES"
```

### 2. Modelo de Ubicación
Editar **`apps/rastreo/models.py`**:
```python
from django.db import models

class UbicacionCamion(models.Model):
    camion_id = models.CharField(max_length=30)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    velocidad = models.DecimalField(max_digits=6, decimal_places=2)
    registrado_en = models.DateTimeField()
    recibido_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.camion_id} - {self.registrado_en}"
```
```bash
python manage.py makemigrations rastreo
python manage.py migrate
```

### 3. Validaciones y Token en Seguridad
Crear **`seguridad/validaciones.py`**:
```python
from decimal import Decimal, InvalidOperation
from django.utils.dateparse import parse_datetime

def convertir_decimal(valor, nombre_campo):
    try:
        return Decimal(str(valor))
    except (InvalidOperation, TypeError):
        raise ValueError(f"El campo {nombre_campo} debe ser numérico.")

def validar_latitud(valor):
    latitud = convertir_decimal(valor, "latitud")
    return latitud

def validar_longitud(valor):
    longitud = convertir_decimal(valor, "longitud")
    return longitud

def validar_velocidad(valor):
    velocidad = convertir_decimal(valor, "velocidad")
    return velocidad

def validar_fecha_hora(valor):
    fecha = parse_datetime(str(valor))
    if fecha is None:
        raise ValueError("El campo registrado_en debe tener formato ISO 8601.")
    return fecha
```

Crear **`seguridad/tokens.py`**:
```python
from django.conf import settings

def obtener_token_bearer(request):
    encabezado = request.headers.get("Authorization", "")
    if not encabezado.startswith("Bearer "):
        return None
    token = encabezado.replace("Bearer ", "", 1).strip()
    if not token:
        return None
    return token

def token_valido(token):
    return token == settings.TOKEN_RASTREO_CAMIONES
```

### 4. Endpoint REST
Editar **`apps/rastreo/views.py`**:
```python
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from seguridad.tokens import obtener_token_bearer, token_valido
from seguridad.validaciones import (
    validar_fecha_hora,
    validar_latitud,
    validar_longitud,
    validar_velocidad,
)
from .models import UbicacionCamion

@csrf_exempt
@require_POST
def registrar_ubicacion(request):
    token = obtener_token_bearer(request)

    if token is None or not token_valido(token):
        return JsonResponse({"error": "Token inválido o ausente."}, status=401)

    try:
        datos = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "El cuerpo debe ser JSON válido."}, status=400)

    camion_id = datos.get("camion_id")

    if not camion_id:
        return JsonResponse({"error": "El campo camion_id es obligatorio."}, status=400)

    try:
        latitud = validar_latitud(datos.get("latitud"))
        longitud = validar_longitud(datos.get("longitud"))
        velocidad = validar_velocidad(datos.get("velocidad"))
        registrado_en = validar_fecha_hora(datos.get("registrado_en"))
    except ValueError as error:
        return JsonResponse({"error": str(error)}, status=400)

    ubicacion = UbicacionCamion.objects.create(
        camion_id=camion_id,
        latitud=latitud,
        longitud=longitud,
        velocidad=velocidad,
        registrado_en=registrado_en
    )

    return JsonResponse(
        {
            "mensaje": "Ubicación registrada correctamente.",
            "ubicacion_id": ubicacion.id
        },
        status=201
    )
```

Crear **`apps/rastreo/urls.py`**:
```python
from django.urls import path
from . import views

urlpatterns = [
    path("api/camiones/ubicacion/", views.registrar_ubicacion, name="registrar_ubicacion"),
]
```

Actualizar **`config/urls.py`**:
```python
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path("", include("apps.bienes.urls")),
    # path("", include("apps.clientes.urls")), # Descomentar si se agregan URLs en clientes posteriormente
    path("", include("apps.rastreo.urls")),
]
```
```