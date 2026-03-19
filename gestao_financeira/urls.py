from django.contrib import admin  # importa o painel administrativo do Django

from django.urls import path, include  # include permite importar rotas de outros apps

urlpatterns = [

    path('admin/', admin.site.urls),  # rota para acessar o painel administrativo

    path('', include('financeiro.urls')),  
    # conecta as rotas do app financeiro ao projeto principal

]