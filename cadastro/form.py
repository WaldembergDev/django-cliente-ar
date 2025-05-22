from django import forms
from .models import Cliente, Ambiente, Endereco

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'cpf_cnpj',
            'nome_razao_social',
            'nome_fantasia',
            'contato',
            'email',
            'telefone_1', 
            'telefone_2',
            ]
        exclude = ['status', 'endereco', 'ambiente']
        labels = {
            'nome_razao_social': 'Nome / Razão Social',
            'cpf_cnpj': 'CPF / CNPJ'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class AmbienteForm(forms.ModelForm):
    class Meta:
        model = Ambiente
        fields = '__all__'
        labels = {
            'area': 'Área (m²)',
            'quantidade_maquinas': 'Quantidade de máquinas (un)'
        }

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = '__all__'
        labels = {
            'cep': 'CEP'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})