from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from seguridad.decorators import cliente_requerido
from .forms import DireccionForm
from .models import Direccion

@login_required
@cliente_requerido
def crear_direccion(request):
    cliente = request.user.cliente
    if request.method == "POST":
        form = DireccionForm(request.POST)
        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.cliente = cliente
            direccion.save()
            return redirect("direcciones:reporte_mis_direcciones")
    else:
        form = DireccionForm()
    return render(request, "direcciones/crear_direccion.html", {"form": form})

@login_required
@cliente_requerido
def reporte_mis_direcciones(request):
    direcciones = Direccion.objects.filter(cliente__usuario=request.user).order_by("-creado_en")
    return render(request, "direcciones/reporte_mis_direcciones.html", {"direcciones": direcciones})
