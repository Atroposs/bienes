from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from seguridad.decorators import auditor_requerido
from seguridad.roles import es_cliente, es_auditor
from apps.bienes.models import Bien
from apps.clientes.models import Cliente

@login_required
def home_router(request):
    """Redirige al usuario a su panel correspondiente según su rol."""
    if es_auditor(request.user):
        return redirect("core:panel_control_auditor")
    elif es_cliente(request.user):
        return redirect("bienes:reporte_mis_bienes")
    else:
        return render(request, "error_rol.html")

@login_required
@auditor_requerido
def panel_control_auditor(request):
    """Panel de control general unificado para el auditor."""
    tab = request.GET.get("tab", "viajes")
    
    # Datos base comunes para el panel
    total_bienes = Bien.objects.count()
    total_clientes = Cliente.objects.filter(usuario__is_active=True).count()
    clientes_pendientes = Cliente.objects.filter(usuario__is_active=False).order_by("-creado_en")

    context = {
        "tab": tab,
        "total_bienes": total_bienes,
        "total_clientes": total_clientes,
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
    else:
        # Vista por defecto: Control de Viajes (representativo)
        bienes = Bien.objects.select_related("cliente").all().order_by("-creado_en")
        context["bienes"] = bienes

    return render(request, "core/panel_control_auditor.html", context)

