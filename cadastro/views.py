from multiprocessing import context
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.messages import constants
from django.contrib import messages

from cadastro.models import Cliente
from cadastro.service import obter_dados_cnpj
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
            # limpando o formulário após salvar os dados
            endereco_form = EnderecoForm()
            ambiente_form = AmbienteForm()
            cliente_form = ClienteForm()
            context = {
                'cliente_form': cliente_form,
                'endereco_form': endereco_form,
                'ambiente_form': ambiente_form,
            }
            messages.add_message(request, constants.SUCCESS, 'O contato foi salvo com sucesso!')
            return redirect('/cadastro/cadastro_cliente')
        return render(request, 'cadastro_cliente.html', context=context)

def consulta_cnpj(request):
    cnpj = request.GET.get('cnpj')
    if not cnpj:
        return JsonResponse({'erro': 'CNPJ não informado'}, status=400)
    dados = obter_dados_cnpj(cnpj)
    if dados:
        return JsonResponse(dados)
    return JsonResponse({'erro': 'CNPJ inválido ou não encontrado'}, status=404)


def lista_cadastros(request):
    cadastros = Cliente.objects.all()
    context = {
        'cadastros': cadastros
    }
    return render(request, 'lista_cadastros.html', context=context)

def listar_unico_cadastro(request, id):
    cadastro = Cliente.objects.filter(id = id).first()
    if request.method == 'GET':        
        cliente_form = ClienteForm(instance = cadastro)
        endereco_form = EnderecoForm(instance = cadastro.endereco)
        ambiente_form = AmbienteForm(instance = cadastro.ambiente)
        context = {
            'cadastro': cliente_form,
            'endereco': endereco_form,
            'ambiente': ambiente_form
        }
        return render(request, 'listar_unico_cadastro.html', context=context)
    else:
        cliente_form = ClienteForm(request.POST, instance=cadastro)
        endereco_form = EnderecoForm(request.POST, instance=cadastro.endereco)
        ambiente_form = AmbienteForm(request.POST, instance=cadastro.ambiente)        
        context = {
            'cliente_form': cliente_form,
            'ambiente_form': ambiente_form,
            'endereco_form': endereco_form
        }
        if endereco_form.is_valid() and ambiente_form.is_valid() and cliente_form.is_valid():
            endereco = endereco_form.save()
            ambiente = ambiente_form.save()
            cliente = cliente_form.save()
            # limpando o formulário após salvar os dados
            endereco_form = EnderecoForm()
            ambiente_form = AmbienteForm()
            cliente_form = ClienteForm()
            context = {
                'cliente_form': cliente_form,
                'endereco_form': endereco_form,
                'ambiente_form': ambiente_form,
            }
            messages.add_message(request, constants.SUCCESS, 'O contato foi atualizado com sucesso!')
            return redirect('listar_unico_cadastro', id=cliente.id)


def visualizacao_kanban(request):
    cadastros = Cliente.objects.all()
    context = {
        'cadastros': cadastros
    }
    return render(request, 'visualizacao_kanban.html', context=context)
         
