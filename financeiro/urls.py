from django.urls import path

from financeiro.views.auth_view import (
    login_view,
    api_login,
    logout_view,
    cadastro_view,
    api_cadastro
)

# HOME
from financeiro.views.auth_view import home_view

# DASHBOARD
from financeiro.views.dashboard_view import (
    dashboard,
    dashboard_dados
)

# RECEITAS
from financeiro.views.receita_view import (
    listar_receitas_view,
    criar_receita_view,
    editar_receita_view,
    excluir_receita_view
)

# DESPESAS
from financeiro.views.despesas_view import (
    listar_despesas_view,
    criar_despesa_view,
    editar_despesa_view,
    excluir_despesa_view
)

# CATEGORIAS
from financeiro.views.categorias_view import (
    listar_categorias_view,
    criar_categoria_view,
    editar_categoria_view,
    excluir_categoria_view
)

app_name = 'financeiro'

urlpatterns = [

    path('', home_view, name='home'),

    # AUTENTICAÇÃO
    path('login/', login_view, name='login'),
    path('api/login/', api_login, name='api_login'),
    path('logout/', logout_view, name='logout'),
    path('cadastro/', cadastro_view, name='cadastro'),
    path('api/cadastro/', api_cadastro, name='api_cadastro'),

    # DASHBOARD
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/dados/', dashboard_dados, name='dashboard_dados'),

    # RECEITAS
    path('receitas/', listar_receitas_view, name='listar_receitas'),
    path('receitas/criar/', criar_receita_view, name='criar_receita'),
    path('receitas/editar/<int:id>/', editar_receita_view, name='editar_receita'),
    path('receitas/excluir/<int:id>/', excluir_receita_view, name='excluir_receita'),

    # DESPESAS
    path('despesas/', listar_despesas_view, name='listar_despesas'),
    path('despesas/criar/', criar_despesa_view, name='criar_despesa'),
    path('despesas/editar/<int:id>/', editar_despesa_view, name='editar_despesa'),
    path('despesas/excluir/<int:id>/', excluir_despesa_view, name='excluir_despesa'),

  
    # CATEGORIAS
    path('categorias/', listar_categorias_view, name='listar_categorias'),
    path('categorias/criar/', criar_categoria_view, name='criar_categoria'),
    path('categorias/editar/<int:id>/', editar_categoria_view, name='editar_categoria'),
    path('categorias/excluir/<int:id>/', excluir_categoria_view, name='excluir_categoria'),
]