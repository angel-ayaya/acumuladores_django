from django import forms
from django.core.exceptions import ValidationError
from .models import QR

class QrForm(forms.ModelForm):
    class Meta:
        model = QR
        fields = ['ClaveAcumulador', 'QR']

    def clean_ClaveAcumulador(self):
        ClaveAcumulador = self.cleaned_data['ClaveAcumulador']
       
        return ClaveAcumulador
