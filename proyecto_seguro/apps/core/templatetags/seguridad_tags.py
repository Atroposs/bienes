from django import template
from seguridad.roles import es_encargado

register = template.Library()

@register.filter(name='is_encargado')
def is_encargado(user):
    return es_encargado(user)
