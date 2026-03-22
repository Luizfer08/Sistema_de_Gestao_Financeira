from django.shortcuts import render, redirect  # renderiza páginas e redireciona

from .models import Receita, Despesa, Categoria  # importa os models

from django.db.models import Sum  # permite somar valores

from datetime import date  # trabalhar com datas


def dashboard(request):
    # função principal do dashboard

    hoje = date.today()
    # pega a data atual

    # SALDO ATUAL
    total_receitas = Receita.objects.filter(usuario=request.user).aggregate(Sum('valor'))['valor__sum'] or 0
    # soma todas receitas

    total_despesas = Despesa.objects.filter(usuario=request.user).aggregate(Sum('valor'))['valor__sum'] or 0
    # soma todas despesas

    saldo_atual = total_receitas - total_despesas
    # calcula saldo atual


    # PREVISÃO
    receitas_futuras = Receita.objects.filter(
        usuario=request.user,
        recorrente=True
    ).aggregate(Sum('valor'))['valor__sum'] or 0
    # soma receitas recorrentes

    despesas_futuras = Despesa.objects.filter(
        usuario=request.user,
        recorrente=True
    ).aggregate(Sum('valor'))['valor__sum'] or 0
    # soma despesas recorrentes

    saldo_futuro = saldo_atual + receitas_futuras - despesas_futuras
    # cálculo final


    # ALERTAS
    alerta = None

    if saldo_futuro < 0:
        alerta = "⚠️ Atenção: Seu saldo futuro será negativo."

    elif despesas_futuras > receitas_futuras:
        alerta = "⚠️ Cuidado: Suas despesas são maiores que suas receitas."

    elif saldo_futuro > 0:
        alerta = "💡 Você terá saldo positivo. Considere investir."

   
    # CONTEXTO
    contexto = {
        'receitas': total_receitas,
        'despesas': total_despesas,
        'saldo': saldo_atual,
        'saldo_futuro': saldo_futuro,
        'alerta': alerta
    }

    return render(request, 'dashboard.html', contexto)


# LISTAR CATEGORIAS
def listar_categorias(request):
    # busca categorias do usuário

    categorias = Categoria.objects.filter(usuario=request.user)

    return render(request, 'categorias/listar.html', {'categorias': categorias})


# CRIAR CATEGORIA
def criar_categoria(request):

    if request.method == 'POST':
        # pega dados do formulário

        nome = request.POST.get('nome')

        Categoria.objects.create(
            nome=nome,
            usuario=request.user
        )
        # salva no banco

        return redirect('listar_categorias')

    return render(request, 'categorias/criar.html')

def criar_receita(request):

    categorias = Categoria.objects.filter(usuario=request.user)
    # busca categorias do usuário

    if request.method == 'POST':

        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data = request.POST.get('data')
        categoria_id = request.POST.get('categoria')

        recorrente = request.POST.get('recorrente') == 'on'
        # verifica se checkbox foi marcado

        data_fim = request.POST.get('data_fim') or None
        # pega data fim (opcional)

        Receita.objects.create(
            descricao=descricao,
            valor=valor,
            data=data,
            categoria_id=categoria_id,
            usuario=request.user,
            recorrente=recorrente,
            data_fim=data_fim
        )

        return redirect('dashboard')

    return render(request, 'receitas/criar.html', {'categorias': categorias})

def criar_despesa(request):

    categorias = Categoria.objects.filter(usuario=request.user)
    # busca categorias do usuário

    if request.method == 'POST':

        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data = request.POST.get('data')
        categoria_id = request.POST.get('categoria')

        recorrente = request.POST.get('recorrente') == 'on'
        # verifica se marcou recorrente

        data_fim = request.POST.get('data_fim') or None
        # pega data fim

        Despesa.objects.create(
            descricao=descricao,
            valor=valor,
            data=data,
            categoria_id=categoria_id,
            usuario=request.user,
            recorrente=recorrente,
            data_fim=data_fim
        )
        # salva no banco

        return redirect('dashboard')

    return render(request, 'despesas/criar.html', {'categorias': categorias})

def listar_receitas(request):
    # busca todas as receitas do usuário logado

    receitas = Receita.objects.filter(usuario=request.user)
    # filtra receitas pelo usuário

    return render(request, 'receitas/listar.html', {'receitas': receitas})
    # envia os dados para o template

def listar_despesas(request):
    # busca todas as despesas do usuário logado

    despesas = Despesa.objects.filter(usuario=request.user)
    # filtra despesas pelo usuário

    return render(request, 'despesas/listar.html', {'despesas': despesas})
    # envia os dados para o template