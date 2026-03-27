from django.urls import path
# função para definir rotas

from . import views
# importa as views do app


urlpatterns = [


    # HOME
    path('', views.home, name='home'),
    # página inicial (login + cadastro)

    # DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),
    # tela principal do sistema

    # RECEITAS
    path('receitas/', views.listar_receitas, name='listar_receitas'),
    path('receitas/criar/', views.criar_receita, name='criar_receita'),
    path('receitas/editar/<int:id>/', views.editar_receita, name='editar_receita'),
    path('receitas/excluir/<int:id>/', views.excluir_receita, name='excluir_receita'),

    # DESPESAS
    path('despesas/', views.listar_despesas, name='listar_despesas'),
    path('despesas/criar/', views.criar_despesa, name='criar_despesa'),
    path('despesas/editar/<int:id>/', views.editar_despesa, name='editar_despesa'),
    path('despesas/excluir/<int:id>/', views.excluir_despesa, name='excluir_despesa'),

    # CATEGORIAS
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/criar/', views.criar_categoria, name='criar_categoria'),


    # API (AJAX
    path('api/login/', views.api_login, name='api_login'),
    path('api/cadastro/', views.api_cadastro, name='api_cadastro'),

]