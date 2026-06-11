from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from seguridad.decorators import cliente_requerido, supervisor_requerido
from seguridad.roles import es_cliente, es_supervisor
from .forms import BienForm
from .models import Bien
from apps.clientes.models import Cliente
from apps.clientes.services import autorizar_cliente_usuario

@login_required
def home_router(request):
    """Redirige al usuario a su panel correspondiente según su rol."""
    if es_supervisor(request.user):
        return redirect("bienes:lista_clientes_supervisor")
    elif es_cliente(request.user):
        return redirect("bienes:reporte_mis_bienes")
    else:
        # Si no tiene rol, lo mandamos a la lista general (que requiere ser supervisor)
        return redirect("bienes:lista_bienes")

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
@supervisor_requerido
def reporte_general_bienes(request):
    bienes = Bien.objects.select_related("cliente").order_by("-creado_en")
    return render(request, "bienes/reporte_general_bienes.html", {"bienes": bienes})

@login_required
@supervisor_requerido
def lista_clientes_supervisor(request):
    """Permite al supervisor listar clientes y ver los bienes de cada uno."""
    # Filtramos clientes activos para la lista lateral y pendientes para la sección de autorizar
    clientes = Cliente.objects.filter(usuario__is_active=True).order_by("nombre")
    clientes_pendientes = Cliente.objects.filter(usuario__is_active=False).order_by("-creado_en")
    cliente_id = request.GET.get("cliente_id")
    bienes = None
    cliente_seleccionado = None

    if cliente_id:
        cliente_seleccionado = get_object_or_404(Cliente, id=cliente_id)
        bienes = Bien.objects.filter(cliente=cliente_seleccionado).order_by("-creado_en")

    return render(
        request,
        "bienes/lista_clientes_supervisor.html",
        {
            "clientes": clientes,
            "clientes_pendientes": clientes_pendientes,
            "cliente_seleccionado": cliente_seleccionado,
            "bienes": bienes,
        },
    )

@login_required
@supervisor_requerido
def autorizar_cliente(request, cliente_id):
    """Vista de acción para autorizar a un cliente desde el panel."""
    cliente = autorizar_cliente_usuario(cliente_id)
    messages.success(request, f"La cuenta de {cliente.nombre_completo} ha sido autorizada.")
    return redirect("bienes:lista_clientes_supervisor")
@login_required
@supervisor_requerido
def lista_bienes(request):
    """Vista de bienes general, ahora solo para supervisores."""
    bienes = Bien.objects.select_related("cliente").all().order_by("-creado_en")
    return render(
        request,
        "bienes/lista_bienes.html",
        {
            "bienes": bienes,
        }
    )
