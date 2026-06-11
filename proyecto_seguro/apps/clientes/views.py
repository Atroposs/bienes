from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ClienteRegistroForm
from .services import registrar_cliente_con_usuario

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