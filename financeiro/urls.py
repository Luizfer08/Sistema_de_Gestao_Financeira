from django.urls import path  # importa sistema de rotas

from . import views  # importa as views do app


urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),
    # rota do dashboard

    path('categorias/', views.listar_categorias, name='listar_categorias'),
    # rota de listagem de categorias

    path('categorias/criar/', views.criar_categoria, name='criar_categoria'),
    # rota para criar uma nova categoria

]