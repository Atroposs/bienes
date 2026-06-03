from django import forms
from .models import Bien
from seguridad.validadores import validar_identificador_bien

class BienForm(forms.ModelForm):
    class Meta:
        model = Bien
        fields = [
            "identificador",
            "descripcion",
            "marca",
            "valor",
            "estatus",
        ]
        widgets = {
            "identificador": forms.TextInput(attrs={"class": "mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border text-slate-900 bg-white"}),
            "descripcion": forms.TextInput(attrs={"class": "mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border text-slate-900 bg-white"}),
            "marca": forms.TextInput(attrs={"class": "mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border text-slate-900 bg-white"}),
            "valor": forms.NumberInput(attrs={"class": "mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border text-slate-900 bg-white", "step": "0.01"}),
            "estatus": forms.Select(attrs={"class": "mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border text-slate-900 bg-white"}),
        }


    def clean_identificador(self):
        identificador = self.cleaned_data["identificador"].strip()
        validar_identificador_bien(identificador)
        return identificador
