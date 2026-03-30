from django.contrib import admin  # admin do Django
from django.urls import path, include  # rotas
from django.contrib.auth import views as auth_views  # login/logout padrão
from financeiro import views  # importa suas views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='home'),
    path('', include('financeiro.urls'))
]

path('resetar-senha/',
     auth_views.PasswordResetView.as_view(
         template_name='senha_reset.html'
     ),
     name='password_reset'),

path('resetar-senha/enviado/',
     auth_views.PasswordResetDoneView.as_view(
         template_name='senha_enviada.html'
     ),
     name='password_reset_done'),

path('resetar/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(
         template_name='nova_senha.html'
     ),
     name='password_reset_confirm'),

path('resetar/concluido/',
     auth_views.PasswordResetCompleteView.as_view(
         template_name='senha_concluida.html'
     ),
     name='password_reset_complete'),



