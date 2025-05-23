from django.urls import path
from . import views

urlpatterns = [
    path('cadastro_cliente', views.cadastro_cliente, name='cadastro_cliente'),
    path('consulta_cnpj/', views.consulta_cnpj , name='consulta_cnpj'),
    path('lista_cadastros', views.lista_cadastros, name='lista_cadastros'),
    path('listar_unico_cadastro/<uuid:id>/', views.listar_unico_cadastro, name='listar_unico_cadastro'),
    path('visualizacao/kanban/', views.visualizacao_kanban, name='visualizacao_kanban'),
    path('atualizar_status/', views.atualizar_status, name='atualizar_status'),
]
