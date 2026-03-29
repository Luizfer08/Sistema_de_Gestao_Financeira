from django.shortcuts import render, redirect, get_object_or_404
# render → exibe templates
# redirect → redireciona
# get_object_or_404 → busca objeto ou retorna 404

from django.contrib.auth.decorators import login_required
# protege rotas (usuário precisa estar logado)

from django.contrib.auth import authenticate, login
# funções de autenticação

from django.contrib.auth.models import User
# modelo padrão de usuário

from django.http import JsonResponse
# resposta JSON (usado no AJAX)

from django.db.models import Sum
# usado para somar valores

from django.views.decorators.csrf import ensure_csrf_cookie
# GARANTE QUE O COOKIE CSRF SEJA CRIADO

from .models import Receita, Despesa, Categoria, Perfil
# seus models

from django.contrib.auth import logout

from django.views.decorators.http import require_POST

from datetime import date

from django.db.models import Sum


# LOGIN PAGE 
@ensure_csrf_cookie
def login_view(request):
    # GARANTE QUE O CSRF FUNCIONE
    return render(request, 'financeiro/autenticacao/login.html')


# HOME
def home(request):
    if request.user.is_authenticated:
        return redirect('financeiro:dashboard')
    return render(request, 'financeiro/home.html')


# DASHBOARD
@login_required
def dashboard(request):

    hoje = date.today()

    # SALDO ATUAL 
    receitas_hoje = Receita.objects.filter(usuario=request.user, data__lte=hoje)
    despesas_hoje = Despesa.objects.filter(usuario=request.user, data__lte=hoje)

    total_receitas_hoje = receitas_hoje.aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas_hoje = despesas_hoje.aggregate(Sum('valor'))['valor__sum'] or 0

    saldo_atual = total_receitas_hoje - total_despesas_hoje

    # DATA FILTRO
    data_filtro = request.GET.get('data')

    if data_filtro:
        data_filtro = date.fromisoformat(data_filtro)
    else:
        data_filtro = hoje

    # DADOS FILTRADOS-
    receitas_filtradas = Receita.objects.filter(
        usuario=request.user,
        data__lte=data_filtro
    )

    despesas_filtradas = Despesa.objects.filter(
        usuario=request.user,
        data__lte=data_filtro
    )

    total_receitas = receitas_filtradas.aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = despesas_filtradas.aggregate(Sum('valor'))['valor__sum'] or 0

    saldo_futuro = total_receitas - total_despesas

    return render(request, 'financeiro/dashboard.html', {
        'saldo': saldo_atual,
        'saldo_futuro': saldo_futuro,
        'receitas': total_receitas,
        'despesas': total_despesas,
        'data_filtro': data_filtro
    })


# RECEITAS
@login_required
def listar_receitas(request):
    receitas = Receita.objects.filter(usuario=request.user)

    return render(request, 'financeiro/receitas/listar.html', {
        'receitas': receitas
    })


@login_required
def criar_receita(request):

    categorias = Categoria.objects.filter(usuario=request.user)

    if request.method == 'POST':

        Receita.objects.create(
            usuario=request.user,
            descricao=request.POST.get('descricao'),
            valor=request.POST.get('valor'),
            data=request.POST.get('data'),
            categoria_id=request.POST.get('categoria'),
            recorrente=True if request.POST.get('recorrente') else False
        )

        return redirect('financeiro:listar_receitas')

    return render(request, 'financeiro/receitas/criar.html', {
        'categorias': categorias
    })


@login_required
def editar_receita(request, id):

    receita = get_object_or_404(Receita, id=id, usuario=request.user)
    categorias = Categoria.objects.filter(usuario=request.user) 

    if request.method == 'POST':
        receita.descricao = request.POST.get('descricao')
        receita.valor = request.POST.get('valor')
        receita.data = request.POST.get('data')
        receita.categoria_id = request.POST.get('categoria')
        receita.save()

        return redirect('financeiro:listar_receitas')

    return render(request, 'financeiro/receitas/editar.html', {
        'receita': receita,
        'categorias': categorias
    })

@require_POST
@login_required
def excluir_receita(request, id):

    receita = get_object_or_404(Receita, id=id, usuario=request.user)
    receita.delete()

    return redirect('financeiro:listar_receitas')


# DESPESAS
@login_required
def listar_despesas(request):

    despesas = Despesa.objects.filter(usuario=request.user)

    return render(request, 'financeiro/despesas/listar.html', {
        'despesas': despesas
    })


@login_required
def criar_despesa(request):

    categorias = Categoria.objects.filter(usuario=request.user)

    if request.method == 'POST':

        Despesa.objects.create(
            usuario=request.user,
            descricao=request.POST.get('descricao'),
            valor=request.POST.get('valor'),
            data=request.POST.get('data'),
            categoria_id=request.POST.get('categoria'),
            recorrente=True if request.POST.get('recorrente') else False
        )

        return redirect('financeiro:listar_despesas')

    return render(request, 'financeiro/despesas/criar.html', {
        'categorias': categorias
    })


@login_required
def editar_despesa(request, id):

    despesa = get_object_or_404(Despesa, id=id, usuario=request.user)
    categorias = Categoria.objects.filter(usuario=request.user)

    if request.method == 'POST':
        despesa.descricao = request.POST.get('descricao')
        despesa.valor = request.POST.get('valor')
        despesa.data = request.POST.get('data')
        despesa.categoria_id = request.POST.get('categoria')
        despesa.save()

        return redirect('financeiro:listar_despesas')

    return render(request, 'financeiro/despesas/editar.html', {
        'despesa': despesa,
        'categorias': categorias
    })

@require_POST
@login_required
def excluir_despesa(request, id):

    despesa = get_object_or_404(Despesa, id=id, usuario=request.user)
    despesa.delete()

    return redirect('financeiro:listar_despesas')


# CATEGORIAS
@login_required
def listar_categorias(request):

    categorias = Categoria.objects.filter(usuario=request.user)

    return render(request, 'financeiro/categorias/listar.html', {
        'categorias': categorias
    })


@login_required
def criar_categoria(request):

    if request.method == 'POST':

        Categoria.objects.create(
            usuario=request.user,
            nome=request.POST.get('nome')
        )

        return redirect('financeiro:listar_categorias')

    return render(request, 'financeiro/categorias/criar.html')


# LOGIN (API AJAX)
@require_POST
def api_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'error': 'Usuário ou senha inválidos'})


# CADASTRO (API)
@require_POST
def api_cadastro(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        aceitou = request.POST.get('aceitou')

        if not aceitou:
            return JsonResponse({'success': False, 'error': 'Aceite os termos'})

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Usuário já existe'})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        perfil, created = Perfil.objects.get_or_create(user=user)
        perfil.aceitou_termos = True
        perfil.save()

        login(request, user)

        return JsonResponse({'success': True})
    
@require_POST
def logout_view(request):
    logout(request)
    return redirect('financeiro:login')

@login_required
def editar_categoria(request, id):

    categoria = get_object_or_404(Categoria, id=id, usuario=request.user)

    if request.method == 'POST':
        categoria.nome = request.POST.get('nome')
        categoria.save()

        return redirect('financeiro:listar_categorias')

    return render(request, 'financeiro/categorias/editar.html', {
        'categoria': categoria
    })

@require_POST
@login_required
def excluir_categoria(request, id):

    categoria = get_object_or_404(Categoria, id=id, usuario=request.user)
    categoria.delete()

    return redirect('financeiro:listar_categorias')