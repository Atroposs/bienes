from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from seguridad.decorators import auditor_requerido
from .forms import ClienteRegistroForm
from .services import registrar_cliente_con_usuario, autorizar_cliente_usuario
from .models import Cliente

def registro(request):
    if request.method == "POST":
        form = ClienteRegistroForm(request.POST)
        if form.is_valid():
            try:
                # Delegamos toda la lógica pesada al servicio
                registrar_cliente_con_usuario(form.cleaned_data)
                
                messages.success(
                    request, 
                    "¡Registro exitoso! Tu cuenta ha sido creada y está en espera de autorización por un administrador."
                )
                return redirect("login")
            except Exception as e:
                # Capturamos cualquier error inesperado del servicio y lo mostramos en el form
                form.add_error(None, f"No se pudo completar el registro: {str(e)}")
    else:
        form = ClienteRegistroForm()
    
    return render(request, "clientes/registro.html", {"form": form})

@login_required
@auditor_requerido
def autorizar_cliente(request, cliente_id):
    """Vista de acción para autorizar a un cliente desde el panel."""
    cliente = autorizar_cliente_usuario(cliente_id)
    messages.success(request, f"La cuenta de {cliente.nombre_completo} ha sido autorizada.")
    return redirect(f"{reverse('bienes:panel_control_auditor')}?tab=clientes")