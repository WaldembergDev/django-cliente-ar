from django.urls import path
from . import views

urlpatterns = [
    path('cadastro_cliente', views.cadastro_cliente, name='cadastro_cliente'),
    path('consulta_cnpj/', views.consulta_cnpj , name='consulta_cnpj'),
    path('lista_cadastros', views.lista_cadastros, name='lista_cadastros')
]
