from django.urls import path
from financeiro import views

app_name = 'financeiro'

urlpatterns = [

    # HOME
    path('', views.home_view, name='home'),

    # AUTH
    path('login/', views.login_view, name='login'),
    path('api/login/', views.api_login, name='api_login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('api/cadastro/', views.api_cadastro, name='api_cadastro'),

    # DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),

    # RECEITAS
    path('receitas/', views.listar_receitas_view, name='listar_receitas'),
    path('receitas/criar/', views.criar_receita_view, name='criar_receita'),
    path('receitas/editar/<int:id>/', views.editar_receita_view, name='editar_receita'),
    path('receitas/excluir/<int:id>/', views.excluir_receita_view, name='excluir_receita'),

    # DESPESAS
    path('despesas/', views.listar_despesas_view, name='listar_despesas'),
    path('despesas/criar/', views.criar_despesa_view, name='criar_despesa'),
    path('despesas/editar/<int:id>/', views.editar_despesa_view, name='editar_despesa'),
    path('despesas/excluir/<int:id>/', views.excluir_despesa_view, name='excluir_despesa'),

    # CATEGORIAS
    path('categorias/', views.listar_categorias_view, name='listar_categorias'),
    path('categorias/criar/', views.criar_categoria_view, name='criar_categoria'),
    path('categorias/editar/<int:id>/', views.editar_categoria_view, name='editar_categoria'),
    path('categorias/excluir/<int:id>/', views.excluir_categoria_view, name='excluir_categoria'),
]