from cProfile import label
from secrets import choice
from django import forms
from . import models

class clienteForm(forms.ModelForm):
    class Meta:
        model = models.Clientes
        fields = '__all__'


class tallerForm(forms.ModelForm):
    class Meta:
        model = models.Talleres
        fields = '__all__'