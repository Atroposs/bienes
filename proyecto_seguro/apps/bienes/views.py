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
