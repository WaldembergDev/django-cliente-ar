from django import forms
from .models import Cliente, Ambiente, Endereco

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        exclude = ['status']

class AmbienteForm(forms.ModelForm):
    class Meta:
        model = Ambiente

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco