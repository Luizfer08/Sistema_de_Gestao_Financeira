from django.urls import path
from . import views

# namespace (OBRIGATÓRIO para usar financeiro:alguma_coisa)
app_name = 'financeiro'

urlpatterns = [


    # HOME 

    path('', views.home, name='home'),
    # ex: /

    path('login/', views.login_view, name='login'),
    # ex: /login/

    path('cadastro/', views.cadastro_view, name='cadastro'),
    # ex: /cadastro/

    path('logout/', views.logout_view, name='logout'),
    # logout via POST


    # API (AJAX)

    path('api/login/', views.api_login, name='api_login'),
    # login via fetch

    path('api/cadastro/', views.api_cadastro, name='api_cadastro'),
    # cadastro via fetch



    # DASHBOARD

    path('dashboard/', views.dashboard, name='dashboard'),
    # ex: /dashboard/


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

    path('categorias/editar/<int:id>/', views.editar_categoria, name='editar_categoria'),

    path('categorias/excluir/<int:id>/', views.excluir_categoria, name='excluir_categoria'),
]