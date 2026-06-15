import re
from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from .models import Camion

class CamionForm(forms.ModelForm):
    class Meta:
        model = Camion
        fields = [
            "placa",
            "identificador",
            "marca",
            "modelo",
            "anio",
            "numero_serie",
            "capacidad_carga_kg",
            "kilometraje_actual",
            "tipo_combustible",
            "estado",
            "activo",
        ]
        widgets = {
            "placa": forms.TextInput(attrs={"class": "mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm px-3 py-2 border text-slate-900 bg-white uppercase", "placeholder": "Ej. ABC-1234"}),
            "identificador": forms.TextInput(attrs={"class": "mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm px-3 py-2 border text-slate-900 bg-white uppercase", "placeholder": "Ej. CAM-001"}),
            "marca": forms.TextInput(attrs={"class": "mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm px-3 py-2 border text-slate-900 bg-white"}),
            "modelo": forms.TextInput(attrs={"class": "mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm px-3 py-2 border text-slate-900 bg-white"}),
            "anio": forms.NumberInput(attrs={"class": "mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm px-3 py-2 border text-slate-900 bg-white"}),
            "numero_serie": forms.TextInput(attrs={"class": "mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm px-3 py-2 border text-slate-900 bg-white uppercase"}),
            "capacidad_carga_kg": forms.NumberInput(attrs={"class": "mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm px-3 py-2 border text-slate-900 bg-white", "step": "0.01"}),
            "kilometraje_actual": forms.NumberInput(attrs={"class": "mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm px-3 py-2 border text-slate-900 bg-white", "step": "0.01"}),
            "tipo_combustible": forms.Select(attrs={"class": "mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm px-3 py-2 border text-slate-900 bg-white"}),
            "estado": forms.Select(attrs={"class": "mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm px-3 py-2 border text-slate-900 bg-white"}),
            "activo": forms.CheckboxInput(attrs={"class": "h-4 w-4 rounded border-slate-300 text-emerald-600 focus:ring-emerald-600"}),
        }

    def clean_placa(self):
        placa = self.cleaned_data["placa"].strip().upper()
        # Formato básico: 1 a 4 letras, un guión (opcional) y 2 a 5 números. O simplemente alfanumérico.
        if not re.match(r'^[A-Z0-9-]{4,10}$', placa):
            raise ValidationError("La placa debe contener entre 4 y 10 caracteres alfanuméricos o guiones.")
        return placa

    def clean_identificador(self):
        return self.cleaned_data["identificador"].strip().upper()
    
    def clean_numero_serie(self):
        return self.cleaned_data["numero_serie"].strip().upper()

    def clean_anio(self):
        anio = self.cleaned_data["anio"]
        anio_actual = date.today().year
        if anio < 1980 or anio > anio_actual + 1:
            raise ValidationError(f"El año debe estar entre 1980 y {anio_actual + 1}.")
        return anio

    def clean_capacidad_carga_kg(self):
        capacidad = self.cleaned_data["capacidad_carga_kg"]
        if capacidad < 0:
            raise ValidationError("La capacidad de carga no puede ser negativa.")
        return capacidad

    def clean_kilometraje_actual(self):
        kilometraje = self.cleaned_data["kilometraje_actual"]
        if kilometraje < 0:
            raise ValidationError("El kilometraje no puede ser negativo.")
        return kilometraje