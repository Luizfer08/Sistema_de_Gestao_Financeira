from django.urls import path
# define rotas

from . import views
# importa todas as views do app


app_name = 'financeiro'
# namespace → evita conflito de nomes


urlpatterns = [

    # HOME
    path('', views.home, name='home'),
    # ex: /

    # DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),
    # ex: /dashboard/

    # RECEITAS
    path('receitas/', views.listar_receitas, name='listar_receitas'),
    # lista receitas

    path('receitas/criar/', views.criar_receita, name='criar_receita'),
    # criar receita

    path('receitas/editar/<int:id>/', views.editar_receita, name='editar_receita'),
    # editar receita

    path('receitas/excluir/<int:id>/', views.excluir_receita, name='excluir_receita'),
    # excluir receita

    # DESPESAS
    path('despesas/', views.listar_despesas, name='listar_despesas'),
    # lista despesas

    path('despesas/criar/', views.criar_despesa, name='criar_despesa'),
    # criar despesa

    path('despesas/editar/<int:id>/', views.editar_despesa, name='editar_despesa'),
    # editar despesa

    path('despesas/excluir/<int:id>/', views.excluir_despesa, name='excluir_despesa'),
    # excluir despesa

    # CATEGORIA
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    # lista categorias

    path('categorias/criar/', views.criar_categoria, name='criar_categoria'),
    # criar categoria
    
    path('api/login/', views.api_login, name='api_login'),
    # login via AJAX

    path('api/cadastro/', views.api_cadastro, name='api_cadastro'),
    # cadastro via AJAX
]