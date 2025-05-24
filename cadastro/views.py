from django.contrib.auth.decorators import login_required
from multiprocessing import context
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.messages import constants
from django.contrib import messages

from cadastro.models import Cliente, StatusEnum
from cadastro.service import obter_dados_cnpj
from .form import ClienteForm, AmbienteForm, EnderecoForm
from django.views.decorators.http import require_POST
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required(login_url='/usuario/login')
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

@login_required(login_url='/usuario/login')
def lista_cadastros(request):
    cadastros = Cliente.objects.all()
    context = {
        'cadastros': cadastros
    }
    return render(request, 'lista_cadastros.html', context=context)

@login_required(login_url='/usuario/login')
def listar_unico_cadastro(request, id):
    cadastro = Cliente.objects.filter(id = id).first()
    if request.method == 'GET':        
        cliente_form = ClienteForm(instance = cadastro)
        endereco_form = EnderecoForm(instance = cadastro.endereco)
        ambiente_form = AmbienteForm(instance = cadastro.ambiente)
        context = {
            'cadastro_form': cliente_form,
            'endereco_form': endereco_form,
            'ambiente_form': ambiente_form,
            'cadastro': cadastro
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

@login_required(login_url='/usuario/login')
def visualizacao_kanban(request):
    pendentes = Cliente.objects.filter(status=StatusEnum.PENDENTE)
    andamento = Cliente.objects.filter(status=StatusEnum.ANDAMENTO)
    concluidos = Cliente.objects.filter(status=StatusEnum.CONCLUIDO)

    context = {
        'pendentes': pendentes,
        'andamento': andamento,
        'concluidos': concluidos,
    }
    return render(request, 'visualizacao_kanban.html', context)

@csrf_exempt
@require_POST
def atualizar_status(request):
    data = json.loads(request.body)
    cliente_id = data.get('id')
    novo_status = data.get('status')

    try:
        cliente = Cliente.objects.get(id=cliente_id)
        cliente.status = novo_status
        cliente.save()
        return JsonResponse({'success': True})
    except Cliente.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cliente não encontrado'})
