from django import forms
from .models import Direccion
from seguridad.validadores import validar_identificador_direccion, validar_codigo_postal

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = [
            "identificador",
            "calle",
            "numero",
            "colonia",
            "ciudad",
            "estado",
            "codigo_postal",
            "tipo",
        ]

    def clean_identificador(self):
        identificador = self.cleaned_data["identificador"].strip()
        validar_identificador_direccion(identificador)
        return identificador
        
    def clean_codigo_postal(self):
        codigo_postal = self.cleaned_data["codigo_postal"].strip()
        validar_codigo_postal(codigo_postal)
        return codigo_postal
