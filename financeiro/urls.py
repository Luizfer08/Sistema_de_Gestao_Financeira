from django.urls import path  # importa sistema de rotas

from . import views  # importa as views do app


urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),
    # rota do dashboard

    path('categorias/', views.listar_categorias, name='listar_categorias'),
    # rota de listagem de categorias

    path('categorias/criar/', views.criar_categoria, name='criar_categoria'),
    # rota para criar uma nova categoria

    path('receitas/criar/', views.criar_receita, name='criar_receita'),

    path('despesas/criar/', views.criar_despesa, name='criar_despesa'),

    path('receitas/', views.listar_receitas, name='listar_receitas'),
    
    path('despesas/', views.listar_despesas, name='listar_despesas'),

]