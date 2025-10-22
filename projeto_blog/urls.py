from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [

    # ADMINISTRATIVO PADRÃO DO DJANGO
    path('admin/', admin.site.urls),
    # PÁGINA INICIAL
    path('', views.index, name='index'),
    # ROTAS DE PROJETOS
    path('projetos/', views.projetos, name='projetos'),  # Lista todos os projetos
    path('projetos/<int:projeto_id>/', views.projeto, name='projeto'),  # Detalhe de um projeto específico
    path('novo_projeto/', views.novo_projeto, name='novo_projeto'),  # Criar novo projeto
    path('editar_projeto/', views.editar_projeto, name='editar_projeto'), # Editar Projeto
    path('projetos/excluir/', views.confirmar_exclusao_projeto_selecao, name='confirmar_exclusao_projeto_selecao'),  # Selecionar projeto para excluir
    path('projetos/excluir/<int:projeto_id>/', views.confirmar_exclusao_projeto, name='confirmar_exclusao_projeto'),  # Confirmar exclusão

    # ROTAS DE POSTAGENS
    path('postagens/', views.lista_postagens, name='postagens'),  # Lista todas as postagens
    path('projetos/<int:projeto_id>/postagens/', views.lista_postagens, name='postagens_por_projeto'),  # Postagens de um projeto específico
    path('postagens/<int:postagem_id>/', views.detalhe_postagem, name='postagem'),  # Detalhe de uma postagem
    path('postagens/<int:postagem_id>/editar/', views.editar_postagem, name='editar_postagem'),  # Editar postagem
    path('nova_postagem/<int:projeto_id>/', views.nova_postagem, name='nova_postagem'),  # Nova postagem vinculada a um projeto
    path('postagens/<int:postagem_id>/excluir/', views.excluir_postagem, name='excluir_postagem'),  # Excluir postagem
    # PÁGINAS INSTITUCIONAIS
    path('sobre/', views.sobre, name='sobre'),  # Página "Sobre"
    path('contato/', views.contato, name='contato'),  # Página "Contato"
    # ROTAS DE USUÁRIOS
    path('users/', include('users.urls')),  # Inclui as rotas do app "users"
]
