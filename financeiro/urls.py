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

    # API (AJAX
    path('api/login/', views.api_login, name='api_login'),
    path('api/cadastro/', views.api_cadastro, name='api_cadastro'),

    path('categorias/', views.listar_categorias, name='listar_categorias'),

    path('receitas/criar/', views.criar_receita, name='criar_receita'),
    
    path('despesas/criar/', views.criar_despesa, name='criar_despesa'),

    path('categorias/criar/', views.criar_categoria, name='criar_categoria'),

]