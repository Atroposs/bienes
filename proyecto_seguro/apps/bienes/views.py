from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def lista_bienes(request):
    return render(request, "bienes/lista.html")


@login_required
def crear_bien(request):
    return render(request, "bienes/formulario.html")
