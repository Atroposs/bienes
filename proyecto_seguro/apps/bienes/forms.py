from django import forms
from .models import Bien

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
