from django import forms
from django.core.exceptions import ValidationError
from .models import QR


from .models import Vehiculo

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['Placas', 'Marca', 'SubMarca', 'SerieChasis', 'Area', 'ClaveAcumulador']

        widgets = {
            'Placas': forms.TextInput(attrs={'class':'form-control'}),
            'Marca': forms.TextInput(attrs={'class':'form-control'}),
            'SubMarca': forms.TextInput(attrs={'class':'form-control'}),
            'SerieChasis': forms.TextInput(attrs={'class':'form-control'}),
            'Area': forms.TextInput(attrs={'class':'form-control'}),
            'ClaveAcumulador': forms.TextInput(attrs={'class':'form-control'}),
        }

        
class QrForm(forms.ModelForm):
    class Meta:
        model = QR
        fields = ['ClaveAcumulador', 'QR']

    def clean_ClaveAcumulador(self):
        ClaveAcumulador = self.cleaned_data['ClaveAcumulador']
       
        return ClaveAcumulador
