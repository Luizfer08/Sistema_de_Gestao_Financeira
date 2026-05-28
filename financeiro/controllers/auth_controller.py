from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse


# API RESPONSÁVEL PELO LOGIN DO USUÁRIO
def api_login(request):

    # Verifica se a requisição é do tipo POST
    if request.method == 'POST':

        # Obtém os dados enviados pelo formulário
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validação de campos obrigatórios
        if not email or not password:
            return JsonResponse({
                'success': False,
                'error': 'Preencha email e senha'
            })

        # Procura usuário pelo email
        try:
            user_obj = User.objects.get(email=email)

        # Caso o email não exista
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Email ou senha inválidos'
            })

        # Autentica utilizando username e senha
        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        # Se autenticado realiza login
        if user:

            login(request, user)
            if request.POST.get('remember'):
                request.session.set_expiry(60 * 60 * 24 * 30)
            else:
                request.session.set_expiry(0)

            return JsonResponse({
                'success': True
            })

        # Caso a senha esteja incorreta
        else:
            return JsonResponse({
                'success': False,
                'error': 'Email ou senha inválidos'
            })

    # Caso o método não seja POST
    return JsonResponse({
        'success': False,
        'error': 'Método inválido'
    })


# API RESPONSÁVEL PELO CADASTRO DE USUÁRIO
def api_cadastro(request):

    # Verifica se a requisição é POST
    if request.method == 'POST':

        # Obtém dados do formulário
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmar = request.POST.get('confirmar')
        aceitou = request.POST.get('aceitou')

        # Validação de campos obrigatórios
        if not username or not email or not password:
            return JsonResponse({
                'success': False,
                'error': 'Preencha todos os campos'
            })

        # Verifica se as senhas coincidem
        if password != confirmar:
            return JsonResponse({
                'success': False,
                'error': 'As senhas não coincidem'
            })

        # Validação de tamanho mínimo da senha
        if len(password) < 6:
            return JsonResponse({
                'success': False,
                'error': 'A senha deve ter pelo menos 6 caracteres'
            })

        # Verifica se os termos foram aceitos
        if aceitou != "true":
            return JsonResponse({
                'success': False,
                'error': 'Aceite os termos'
            })

        # Verifica se o email já existe
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'error': 'Email já cadastrado'
            })

        # Cria usuário no banco de dados
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Realiza login automático após cadastro
        login(request, user)

        return JsonResponse({
            'success': True
        })

    # Caso o método não seja POST
    return JsonResponse({
        'success': False,
        'error': 'Método inválido'
    })


# VIEW DA TELA DE LOGIN
def login_view(request):

    # Se já estiver autenticado redireciona ao dashboard
    if request.user.is_authenticated:
        return redirect('financeiro:dashboard')

    # Renderiza página de login
    return render(
        request,
        'financeiro/autenticacao/login.html'
    )


# VIEW DA TELA DE CADASTRO
def cadastro_view(request):

    # Se já estiver autenticado redireciona ao dashboard
    if request.user.is_authenticated:
        return redirect('financeiro:dashboard')

    # Renderiza página de cadastro
    return render(
        request,
        'financeiro/autenticacao/cadastro.html'
    )

# REALIZA LOGOUT DO USUÁRIO
def logout_view(request):

    # Encerra sessão do usuário
    logout(request)

    # Redireciona para tela de login
    return redirect('financeiro:login')

# VIEW INICIAL DO SISTEMA
def home_view(request):

    # Se usuário estiver autenticado
    if request.user.is_authenticated:

        # Redireciona para dashboard
        return redirect('financeiro:dashboard')

    # Caso contrário redireciona para login
    return redirect('financeiro:login')
