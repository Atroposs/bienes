from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from seguridad.decorators import auditor_requerido
from .forms import CamionForm
from .models import Camion

@login_required
@auditor_requerido
def crear_camion(request):
    """Vista para registrar un nuevo camión."""
    if request.method == "POST":
        form = CamionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Camión registrado exitosamente.")
            return redirect("core:panel_control_auditor", permanent=False)
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = CamionForm()
    
    return render(request, "camiones/formulario_camion.html", {
        "form": form,
        "titulo": "Registrar Nuevo Camión",
        "btn_texto": "Registrar Camión",
    })

@login_required
@auditor_requerido
def editar_camion(request, pk):
    """Vista para editar un camión existente."""
    camion = get_object_or_404(Camion, pk=pk)
    if request.method == "POST":
        form = CamionForm(request.POST, instance=camion)
        if form.is_valid():
            form.save()
            messages.success(request, f"Camión {camion.placa} actualizado exitosamente.")
            return redirect(f"/general/?tab=camiones")
    else:
        form = CamionForm(instance=camion)
    
    return render(request, "camiones/formulario_camion.html", {
        "form": form,
        "titulo": f"Editar Camión: {camion.placa}",
        "btn_texto": "Guardar Cambios",
    })

