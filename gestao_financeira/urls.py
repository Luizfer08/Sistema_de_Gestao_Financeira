# Admin do Django
from django.contrib import admin

# Rotas
from django.urls import path, include

# Views padrão do Django (reset de senha)
from django.contrib.auth import views as auth_views

from financeiro.controllers.auth_controller import login_view


urlpatterns = [

    # ADMIN
    path('admin/', admin.site.urls),

    # HOME (login)
    path('', login_view, name='home'),

    # APP FINANCEIRO
    path('', include('financeiro.urls')),

    # RESET DE SENHA

    path('resetar-senha/',
         auth_views.PasswordResetView.as_view(
             template_name='financeiro/autenticacao/senha_reset.html'
         ),
         name='password_reset'),

    path('resetar-senha/enviado/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='financeiro/autenticacao/senha_enviada.html'
         ),
         name='password_reset_done'),

    path('resetar/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='financeiro/autenticacao/nova_senha.html'
         ),
         name='password_reset_confirm'),

    path('resetar/concluido/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='financeiro/autenticacao/senha_concluida.html'
         ),
         name='password_reset_complete'),
]