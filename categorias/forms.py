# forms.py
from django import forms
from .models import *

class CategoriaImpactoForm(forms.ModelForm):
    class Meta:
        model = CategoriaImpacto
        fields = '__all__'  
        

class CategoriaStatusForm(forms.ModelForm):
    class Meta:
        model = CategoriaStatus
        fields = '__all__'  