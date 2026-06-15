import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Empleado, UbicacionEmpleado
from seguridad.decorators import auditor_requerido
from seguridad.roles import es_encargado

@csrf_exempt
@login_required
def actualizar_ubicacion(request):
    if request.method == "POST":
        if not es_encargado(request.user):
            return JsonResponse({"error": "No tienes permisos de encargado."}, status=403)
        
        try:
            data = json.loads(request.body)
            latitud = data.get("latitud")
            longitud = data.get("longitud")
            
            if latitud is None or longitud is None:
                return JsonResponse({"error": "Latitud y longitud requeridos."}, status=400)
            
            # Buscamos el empleado asociado a este usuario
            empleado = getattr(request.user, "empleado", None)
            if not empleado:
                return JsonResponse({"error": "No hay registro de empleado para este usuario."}, status=404)
            
            # Guardamos la ubicación para trazabilidad
            UbicacionEmpleado.objects.create(
                empleado=empleado,
                latitud=latitud,
                longitud=longitud
            )
            
            return JsonResponse({"status": "success", "message": "Ubicación actualizada"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)

@login_required
@auditor_requerido
def listar_ubicaciones(request):
    if request.method == "GET":
        empleados_activos = Empleado.objects.filter(activo=True, puesto="encargado")
        
        resultados = []
        for empleado in empleados_activos:
            ultima_ub = empleado.ubicaciones.first()  # Gracias al ordering = ['-registrado_en']
            if ultima_ub:
                resultados.append({
                    "id": empleado.identificador,
                    "nombre": empleado.nombre_completo,
                    "latitud": float(ultima_ub.latitud),
                    "longitud": float(ultima_ub.longitud),
                    "actualizado_en": ultima_ub.registrado_en.strftime("%Y-%m-%d %H:%M:%S")
                })
                
        return JsonResponse({"status": "success", "data": resultados})
    return JsonResponse({"error": "Método no permitido"}, status=405)

@login_required
def panel_encargado(request):
    if not es_encargado(request.user):
        return redirect("core:home_router")
    
    empleado = getattr(request.user, "empleado", None)
    return render(request, "empleados/panel_encargado.html", {"empleado": empleado})
