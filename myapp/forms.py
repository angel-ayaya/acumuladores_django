"""Formularios"""
from django import forms

from .models import Vehiculo

class VehiculoForm(forms.ModelForm):
    """Formulario para el modelo Vehiculo"""
    class Meta:
        model = Vehiculo
        fields = ['Placas', 'Marca', 'SubMarca', 'SerieChasis', 'Area', 'ClaveAcumulador']

        widgets = {
            'Placas': forms.TextInput(attrs={'class':'form-control'} ),
            'Marca': forms.TextInput(attrs={'class':'form-control'}),
            'SubMarca': forms.TextInput(attrs={'class':'form-control'}),
            'SerieChasis': forms.TextInput(attrs={'class':'form-control'}),
            'Area': forms.TextInput(attrs={'class':'form-control'}),
            'ClaveAcumulador': forms.TextInput(attrs={'class':'form-control', }),
            # add 'disabled': '' to the attrs dict if you don't want the field editable
        }
