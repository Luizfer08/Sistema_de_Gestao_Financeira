from django.contrib import admin  # admin do Django
from django.urls import path, include  # rotas
from django.contrib.auth import views as auth_views  # login/logout padrão
from financeiro import views  # importa suas views


urlpatterns = [

    path('', views.home, name='home'),

    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    #  HOME (rota padrão)

    path('', include('financeiro.urls')),
    # rotas do app

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
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

