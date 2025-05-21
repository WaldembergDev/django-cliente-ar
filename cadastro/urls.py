from django.urls import path
from . import views

urlpatterns = [
    path('cadastro_cliente', views.cadastro_cliente, name='cadastro_cliente')
]
