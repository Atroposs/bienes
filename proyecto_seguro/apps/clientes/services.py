from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth.models import User, Group
from seguridad.roles import GRUPO_CLIENTE
from .models import Cliente

def registrar_cliente_con_usuario(datos_registro):
    """
    Servicio que orquestra la creación de un Usuario de Django y su perfil de Cliente.
    Encapsula la transacción atómica, asignación de roles y estado inicial.
    """
    with transaction.atomic():
        # 1. Crear el usuario de autenticación (deshabilitado por defecto)
        user = User.objects.create_user(
            username=datos_registro["username"],
            password=datos_registro["password"],
            email=datos_registro["correo"],
            is_active=False
        )

        # 2. Garantizar que el grupo exista y asignarlo
        grupo, _ = Group.objects.get_or_create(name=GRUPO_CLIENTE)
        user.groups.add(grupo)

        # 3. Crear el perfil de Cliente vinculado al usuario
        return Cliente.objects.create(
            usuario=user,
            identificador=datos_registro["identificador"],
            nombre=datos_registro["nombre"],
            apellido_paterno=datos_registro["apellido_paterno"],
            apellido_materno=datos_registro["apellido_materno"],
            correo=datos_registro["correo"],
            telefono=datos_registro["telefono"]
        )

def autorizar_cliente_usuario(cliente_id):
    """Activa la cuenta de un usuario para que pueda iniciar sesión."""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    user = cliente.usuario
    user.is_active = True
    user.save()
    return cliente