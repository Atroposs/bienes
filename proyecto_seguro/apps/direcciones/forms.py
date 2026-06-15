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
        help_texts = {
            'identificador': 'Formato d-XXXX-año (ej. d-0001-2024).',
            'codigo_postal': 'Debe contener exactamente 5 dígitos.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicamos clases de Tailwind de forma masiva a todos los campos
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'block w-full rounded-lg border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm'
            })
        
        # Limitaciones específicas para Identificador (acorde a tu Regex d-\d{4}-\d{4})
        self.fields['identificador'].widget.attrs.update({
            'placeholder': 'd-0001-2024',
            'maxlength': '11',
            'minlength': '11',
            'pattern': r'd-\d{4}-\d{4}',
            'title': 'El formato debe ser d-XXXX-año (11 caracteres)'
        })
        
        # Limitaciones para Código Postal (acorde a tu Regex \d{5})
        self.fields['codigo_postal'].widget.attrs.update({
            'placeholder': '12345',
            'maxlength': '5',
            'minlength': '5',
            'pattern': r'\d{5}',
            'title': 'Debe ser un código postal de 5 dígitos'
        })

        # Placeholder para otros campos comunes
        if 'calle' in self.fields:
            self.fields['calle'].widget.attrs['placeholder'] = 'Av. Principal'
        if 'numero' in self.fields:
            self.fields['numero'].widget.attrs['placeholder'] = '123-A'

    def clean_identificador(self):
        identificador = self.cleaned_data["identificador"].strip()
        validar_identificador_direccion(identificador)
        return identificador
        
    def clean_codigo_postal(self):
        codigo_postal = self.cleaned_data["codigo_postal"].strip()
        validar_codigo_postal(codigo_postal)
        return codigo_postal
