from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from seguridad.decorators import cliente_requerido, auditor_requerido
from seguridad.roles import es_cliente, es_auditor
from .forms import BienForm
from .models import Bien
from apps.clientes.models import Cliente


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
            return redirect("bienes:reporte_mis_bienes")
    else:
        form = BienForm()
    return render(request, "bienes/crear_bien.html", {"form": form})

@login_required
@cliente_requerido
def reporte_mis_bienes(request):
    bienes = Bien.objects.filter(cliente__usuario=request.user).order_by("-creado_en")
    return render(request, "bienes/reporte_mis_bienes.html", {"bienes": bienes})

@login_required
@auditor_requerido
def reporte_general_bienes(request):
    bienes = Bien.objects.select_related("cliente").order_by("-creado_en")
    return render(request, "bienes/reporte_general_bienes.html", {"bienes": bienes})

@login_required
@auditor_requerido
def lista_bienes(request):
    """Vista de bienes general, ahora solo para supervisores."""
    bienes = Bien.objects.select_related("cliente").all().order_by("-creado_en")
    return render(
        request,
        "bienes/lista_bienes.html",
        {
            "bienes": bienes,
            "es_auditor": True,
            "es_cliente": False,
        }
    )

