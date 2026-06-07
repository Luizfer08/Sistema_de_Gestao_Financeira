# Render e redirect devolvem paginas HTML ou redirecionam o usuario.
from django.shortcuts import render, redirect

# Messages exibe feedback na tela de alteracao de dados.
from django.contrib import messages

# Funcoes de autenticacao do Django.
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

# Login_required protege telas que precisam de usuario autenticado.
from django.contrib.auth.decorators import login_required

# User e o model padrao de usuarios do Django.
from django.contrib.auth.models import User

# JsonResponse devolve respostas para requisicoes AJAX.
from django.http import JsonResponse

# Require_POST garante que a exclusao de usuario use somente POST.
from django.views.decorators.http import require_POST

# AceiteTermos registra que o usuario aceitou os termos ao criar a conta.
from financeiro.models import AceiteTermos


# API usada pelo formulario de login.
def api_login(request):

    # Login deve ser feito apenas por POST.
    if request.method == 'POST':

        # Dados enviados pelo formulario.
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Campos obrigatorios.
        if not email or not password:
            return JsonResponse({
                'success': False,
                'error': 'Preencha email e senha'
            })

        # O usuario faz login com email, mas o Django autentica por username.
        try:
            user_obj = User.objects.get(email=email)

        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Email ou senha invalidos'
            })

        # Autentica usando o username encontrado pelo email.
        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        # Se a senha estiver correta, inicia a sessao.
        if user:

            login(request, user)

            # Lembrar de mim aumenta a duracao da sessao.
            if request.POST.get('remember'):
                request.session.set_expiry(60 * 60 * 24 * 30)
            else:
                request.session.set_expiry(0)

            return JsonResponse({
                'success': True
            })

        return JsonResponse({
            'success': False,
            'error': 'Email ou senha invalidos'
        })

    return JsonResponse({
        'success': False,
        'error': 'Metodo invalido'
    })


# API usada pelo formulario de cadastro.
def api_cadastro(request):

    # Cadastro deve ser feito apenas por POST.
    if request.method == 'POST':

        # Dados enviados pelo formulario.
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmar = request.POST.get('confirmar')
        aceitou = request.POST.get('aceitou')

        # Valida campos principais.
        if not username or not email or not password:
            return JsonResponse({
                'success': False,
                'error': 'Preencha todos os campos'
            })

        # Confirma se as duas senhas sao iguais.
        if password != confirmar:
            return JsonResponse({
                'success': False,
                'error': 'As senhas nao coincidem'
            })

        # Senha minima para evitar senhas muito fracas.
        if len(password) < 6:
            return JsonResponse({
                'success': False,
                'error': 'A senha deve ter pelo menos 6 caracteres'
            })

        # O cadastro so avanca se os termos forem aceitos.
        if aceitou != "true":
            return JsonResponse({
                'success': False,
                'error': 'Aceite os termos'
            })

        # Evita cadastro duplicado com o mesmo email.
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'error': 'Email ja cadastrado'
            })

        # Cria o usuario com senha criptografada pelo Django.
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Salva no banco que o usuario aceitou os termos.
        AceiteTermos.objects.create(
            usuario=user,
            aceitou=True,
            versao='2026-05-28'
        )

        # Apos cadastrar, o usuario ja entra no sistema.
        login(request, user)

        return JsonResponse({
            'success': True
        })

    return JsonResponse({
        'success': False,
        'error': 'Metodo invalido'
    })


# Renderiza a tela de login.
def login_view(request):

    # Usuario logado nao precisa ver login novamente.
    if request.user.is_authenticated:
        return redirect('financeiro:dashboard')

    return render(
        request,
        'financeiro/autenticacao/login.html'
    )


# Renderiza a tela de cadastro.
def cadastro_view(request):

    # Usuario logado e enviado direto para o dashboard.
    if request.user.is_authenticated:
        return redirect('financeiro:dashboard')

    return render(
        request,
        'financeiro/autenticacao/cadastro.html'
    )


# Renderiza a pagina publica de termos de uso e privacidade.
def termos_view(request):

    return render(
        request,
        'financeiro/autenticacao/termos.html'
    )


# Encerra a sessao do usuario.
def logout_view(request):

    logout(request)

    return redirect('financeiro:login')


# Exclui o usuario logado e todos os dados vinculados a ele.
@login_required
@require_POST
def excluir_usuario_view(request):

    usuario = request.user

    # Encerra a sessao antes de apagar a conta.
    logout(request)

    usuario.delete()

    return redirect('financeiro:login')


# Permite alterar nome de usuario e senha, mantendo o email bloqueado.
@login_required
def alterar_dados_view(request):

    usuario = request.user

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirmar = request.POST.get('confirmar', '')

        # Nome de usuario e obrigatorio.
        if not username:
            messages.error(request, 'Informe o nome de usuario.')
            return redirect('financeiro:alterar_dados')

        # Evita que dois usuarios tenham o mesmo username.
        if (
            User.objects
            .filter(username=username)
            .exclude(id=usuario.id)
            .exists()
        ):
            messages.error(request, 'Esse nome de usuario ja esta em uso.')
            return redirect('financeiro:alterar_dados')

        # Senha e opcional; so altera se algum campo de senha for preenchido.
        if password or confirmar:

            if password != confirmar:
                messages.error(request, 'As senhas nao coincidem.')
                return redirect('financeiro:alterar_dados')

            if len(password) < 6:
                messages.error(
                    request,
                    'A senha deve ter pelo menos 6 caracteres.'
                )
                return redirect('financeiro:alterar_dados')

            # Set_password aplica a criptografia da senha.
            usuario.set_password(password)

            # Mantem o usuario logado apos trocar a senha.
            update_session_auth_hash(request, usuario)

        usuario.username = username
        usuario.save()

        messages.success(request, 'Dados alterados com sucesso.')
        return redirect('financeiro:alterar_dados')

    return render(
        request,
        'financeiro/usuario/alterar_dados.html'
    )


# Decide a primeira tela do sistema.
def home_view(request):

    # Usuario autenticado entra no dashboard.
    if request.user.is_authenticated:

        return redirect('financeiro:dashboard')

    # Visitante e enviado para o login.
    return redirect('financeiro:login')
