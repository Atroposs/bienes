from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from seguridad.decorators import cliente_requerido, auditor_requerido
from seguridad.roles import es_cliente, es_auditor
from .forms import BienForm
from .models import Bien
from apps.clientes.models import Cliente
from apps.camiones.models import Camion

@login_required
def home_router(request):
    """Redirige al usuario a su panel correspondiente según su rol."""
    if es_auditor(request.user):
        return redirect("bienes:panel_control_auditor")
    elif es_cliente(request.user):
        return redirect("bienes:reporte_mis_bienes")
    else:
        return render(request, "error_rol.html")

@login_required
@auditor_requerido
def panel_control_auditor(request):
    """Panel de control general unificado para el auditor."""
    tab = request.GET.get("tab", "viajes")
    
    # Datos base para el panel
    total_bienes = Bien.objects.count()
    total_clientes = Cliente.objects.filter(usuario__is_active=True).count()
    total_camiones = Camion.objects.count()
    clientes_pendientes = Cliente.objects.filter(usuario__is_active=False).order_by("-creado_en")

    context = {
        "tab": tab,
        "total_bienes": total_bienes,
        "total_clientes": total_clientes,
        "total_camiones": total_camiones,
        "clientes_pendientes": clientes_pendientes,
    }

    if tab == "clientes":
        clientes = Cliente.objects.filter(usuario__is_active=True).order_by("nombre")
        cliente_id = request.GET.get("cliente_id")
        bienes_cliente = None
        cliente_seleccionado = None
        if cliente_id:
            cliente_seleccionado = get_object_or_404(Cliente, id=cliente_id)
            bienes_cliente = Bien.objects.filter(cliente=cliente_seleccionado).order_by("-creado_en")
        context.update({
            "clientes": clientes,
            "cliente_seleccionado": cliente_seleccionado,
            "bienes_cliente": bienes_cliente,
        })
    elif tab == "camiones":
        context.update({"camiones": Camion.objects.all().order_by("-creado_en")})
    else:
        # Viajes (representativo por ahora)
        context["bienes"] = Bien.objects.select_related("cliente").all().order_by("-creado_en")

    return render(request, "bienes/panel_control_auditor.html", context)


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
