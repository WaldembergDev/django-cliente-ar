from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib import messages
from django.contrib.messages import constants
from .models import Usuario

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect("/cadastro/cadastro_cliente")
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        login = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, username=login, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect('/cadastro/cadastro_cliente')
            else:
                messages.add_message(request, constants.ERROR, 'Usuário inativo no sistema!')
                return redirect('/usuario/login') # usuário está inativo
        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos!')
            return redirect('/usuario/login') # senha errada

def logout(request):
    auth.logout(request)
    return redirect('/usuario/login')
