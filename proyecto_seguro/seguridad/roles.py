GRUPO_CLIENTE = "cliente"
GRUPO_SUPERVISOR = "supervisor"

def pertenece_a_grupo(user, nombre_grupo):
    return user.is_authenticated and user.groups.filter(name=nombre_grupo).exists()

def es_cliente(user):
    if not user.is_authenticated:
        return False
    return pertenece_a_grupo(user, GRUPO_CLIENTE)

def es_supervisor(user):
    if not user.is_authenticated:
        return False
    # Un superusuario (admin) también actúa como supervisor por defecto
    return user.is_superuser or pertenece_a_grupo(user, GRUPO_SUPERVISOR)
