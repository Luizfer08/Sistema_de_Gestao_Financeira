from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse


def api_login(request):

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return JsonResponse({
                'success': False,
                'error': 'Preencha email e senha'
            })

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Email ou senha inválidos'
            })

        user = authenticate(request, username=user_obj.username, password=password)

        if user:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({
                'success': False,
                'error': 'Email ou senha inválidos'
            })

    return JsonResponse({
        'success': False,
        'error': 'Método inválido'
    })


def api_cadastro(request):

    if request.method == 'POST':

        username = request.POST.get('username')  # 👈 nome do usuário
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmar = request.POST.get('confirmar')
        aceitou = request.POST.get('aceitou')


        if not username or not email or not password:
            return JsonResponse({
                'success': False,
                'error': 'Preencha todos os campos'
            })

        if password != confirmar:
            return JsonResponse({
                'success': False,
                'error': 'As senhas não coincidem'
            })

        if len(password) < 6:
            return JsonResponse({
                'success': False,
                'error': 'A senha deve ter pelo menos 6 caracteres'
            })

        if aceitou != "true":
            return JsonResponse({
                'success': False,
                'error': 'Aceite os termos'
            })

        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'error': 'Email já cadastrado'
            })

        user = User.objects.create_user(
            username=username,  
            email=email,
            password=password
        )

        # LOGIN AUTOMÁTICO
        login(request, user)

        return JsonResponse({'success': True})

    return JsonResponse({
        'success': False,
        'error': 'Método inválido'
    })

def login_view(request):

    if request.user.is_authenticated:
        return redirect('financeiro:dashboard')

    return render(request, 'financeiro/autenticacao/login.html')

def cadastro_view(request):

    if request.user.is_authenticated:
        return redirect('financeiro:dashboard')

    return render(request, 'financeiro/autenticacao/cadastro.html')

def logout_view(request):

    logout(request)
    return redirect('financeiro:login')

def home_view(request):

    if request.user.is_authenticated:
        return redirect('financeiro:dashboard')

    return redirect('financeiro:login')