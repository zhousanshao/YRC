# forms.py
from django import forms
from .models import Honor

class HonorForm(forms.ModelForm):
    class Meta:
        model = Honor
        fields = ['name', 'motto', 'photo', 'honor_type', 'date_achieved']
        widgets = {
            'date_achieved': forms.DateInput(attrs={'type': 'date'}),
        }