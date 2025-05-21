from django.http import HttpResponse
from django.shortcuts import redirect, render
from .form import ClienteForm, AmbienteForm, EnderecoForm

# Create your views here.
def cadastro_cliente(request):
    if request.method == 'GET':
        endereco_form = EnderecoForm()
        ambiente_form = AmbienteForm()
        cliente_form = ClienteForm()
        context = {'cliente_form': cliente_form,
                   'endereco_form': endereco_form,
                   'ambiente_form': ambiente_form}
        return render(request, 'cadastro_cliente.html', context=context)
    else:
        endereco_form = EnderecoForm(request.POST)
        ambiente_form = AmbienteForm(request.POST)
        cliente_form = ClienteForm(request.POST)
        context = {'cliente_form': cliente_form,
                   'endereco_form': endereco_form,
                   'ambiente_form': ambiente_form}
        if endereco_form.is_valid() and ambiente_form.is_valid() and cliente_form.is_valid():
            endereco = endereco_form.save()
            ambiente = ambiente_form.save()
            cliente = cliente_form.save(commit=False)
            cliente.endereco = endereco
            cliente.ambiente = ambiente
            cliente.save()
            return HttpResponse('Formulário criado com sucesso!')
        return render(request, 'cadastro_cliente.html', context=context)
            