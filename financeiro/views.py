from django.shortcuts import render, redirect, get_object_or_404
# renderiza páginas

from django.contrib.auth.decorators import login_required
# protege rotas

from django.contrib.auth import authenticate, login
# autenticação

from django.contrib.auth.models import User
# modelo de usuário

from django.http import JsonResponse
# respostas JSON (AJAX)

from django.db.models import Sum
# somar valores

from .models import Receita, Despesa, Categoria, Perfil
# seus models


# HOME
def home(request):
    return render(request, 'home.html')


# DASHBOARD
@login_required
def dashboard(request):

    # garante perfil (evita erro)
    perfil, created = Perfil.objects.get_or_create(user=request.user)

    # LGPD
    if not perfil.aceitou_termos:
        return redirect('home')

    receitas = Receita.objects.filter(usuario=request.user)
    despesas = Despesa.objects.filter(usuario=request.user)

    total_receitas = receitas.aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = despesas.aggregate(Sum('valor'))['valor__sum'] or 0

    saldo = total_receitas - total_despesas

    return render(request, 'dashboard.html', {
        'saldo': saldo,
        'receitas': total_receitas,
        'despesas': total_despesas
    })


# RECEITAS
@login_required
def listar_receitas(request):

    receitas = Receita.objects.filter(usuario=request.user)
    return render(request, 'receitas/listar.html', {'receitas': receitas})


@login_required
def criar_receita(request):

    categorias = Categoria.objects.filter(usuario=request.user)

    if request.method == 'POST':

        Receita.objects.create(
            usuario=request.user,
            descricao=request.POST.get('descricao'),  # 🔥 corrigido
            valor=request.POST.get('valor'),
            categoria_id=request.POST.get('categoria'),
            recorrente=True if request.POST.get('recorrente') else False
        )

        return redirect('listar_receitas')

    return render(request, 'receitas/criar.html', {
        'categorias': categorias
    })


@login_required
def editar_receita(request, id):

    receita = get_object_or_404(Receita, id=id, usuario=request.user)

    if request.method == 'POST':
        receita.descricao = request.POST.get('descricao')
        receita.valor = request.POST.get('valor')
        receita.save()
        return redirect('listar_receitas')

    return render(request, 'receitas/editar.html', {'receita': receita})


@login_required
def excluir_receita(request, id):

    receita = get_object_or_404(Receita, id=id, usuario=request.user)
    receita.delete()
    return redirect('listar_receitas')


# DESPESAS
@login_required
def listar_despesas(request):

    despesas = Despesa.objects.filter(usuario=request.user)
    return render(request, 'despesas/listar.html', {'despesas': despesas})


@login_required
def criar_despesa(request):

    categorias = Categoria.objects.filter(usuario=request.user)

    if request.method == 'POST':

        Despesa.objects.create(
            usuario=request.user,
            descricao=request.POST.get('descricao'),  # 🔥 alinhado
            valor=request.POST.get('valor'),
            categoria_id=request.POST.get('categoria'),
            recorrente=True if request.POST.get('recorrente') else False
        )

        return redirect('listar_despesas')

    return render(request, 'despesas/criar.html', {
        'categorias': categorias
    })


@login_required
def editar_despesa(request, id):

    despesa = get_object_or_404(Despesa, id=id, usuario=request.user)

    if request.method == 'POST':
        despesa.descricao = request.POST.get('descricao')
        despesa.valor = request.POST.get('valor')
        despesa.save()
        return redirect('listar_despesas')

    return render(request, 'despesas/editar.html', {'despesa': despesa})


@login_required
def excluir_despesa(request, id):

    despesa = get_object_or_404(Despesa, id=id, usuario=request.user)
    despesa.delete()
    return redirect('listar_despesas')


# CATEGORIAS
@login_required
def listar_categorias(request):

    categorias = Categoria.objects.filter(usuario=request.user)
    return render(request, 'categorias/listar.html', {'categorias': categorias})


@login_required
def criar_categoria(request):

    if request.method == 'POST':
        Categoria.objects.create(
            usuario=request.user,
            nome=request.POST.get('nome')
        )
        return redirect('listar_categorias')

    return render(request, 'categorias/criar.html')


# API LOGIN (AJAX)
def api_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'error': 'Usuário ou senha inválidos'})


# API CADASTRO (AJAX + LGPD)
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

        perfil = Perfil.objects.get(user=user)
        perfil.aceitou_termos = True
        perfil.save()

        login(request, user)

        return JsonResponse({'success': True})