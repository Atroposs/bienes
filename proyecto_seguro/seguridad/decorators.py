from functools import wraps
from django.core.exceptions import PermissionDenied
from .roles import es_cliente, es_auditor

def auditor_requerido(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not es_auditor(request.user):
            raise PermissionDenied("Se requiere rol de auditor.")
        return view_func(request, *args, **kwargs)
    return wrapper

def cliente_requerido(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not es_cliente(request.user):
            raise PermissionDenied("Se requiere rol de cliente.")
        return view_func(request, *args, **kwargs)
    return wrapper
