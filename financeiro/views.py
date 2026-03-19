from django.shortcuts import render  # função que renderiza páginas HTML

from .models import Receita, Despesa, Categoria  # importa os modelos do banco de dados

from django.db.models import Sum  # permite fazer cálculos no banco de dados


def dashboard(request):
    # função responsável por montar os dados exibidos no dashboard

    total_receitas = Receita.objects.filter(usuario=request.user).aggregate(Sum('valor'))['valor__sum'] or 0
    # soma todas as receitas do usuário logado

    total_despesas = Despesa.objects.filter(usuario=request.user).aggregate(Sum('valor'))['valor__sum'] or 0
    # soma todas as despesas do usuário logado

    saldo_total = total_receitas - total_despesas
    # calcula o saldo financeiro

    contexto = {
        'receitas': total_receitas,
        'despesas': total_despesas,
        'saldo': saldo_total
    }
    # envia os dados para o template

    return render(request, 'dashboard.html', contexto)
    # renderiza a página dashboard.html


def listar_categorias(request):
    # função responsável por listar todas as categorias do usuário

    categorias = Categoria.objects.filter(usuario=request.user)
    # busca no banco todas as categorias relacionadas ao usuário

    return render(request, 'categorias/listar.html', {'categorias': categorias})
    # renderiza a página de listagem de categorias


def criar_categoria(request):
    # função responsável por cadastrar uma nova categoria

    if request.method == 'POST':
        # verifica se o usuário enviou o formulário

        nome = request.POST.get('nome')
        # pega o valor do campo nome enviado pelo formulário

        Categoria.objects.create(
            nome=nome,
            usuario=request.user
        )
        # cria uma nova categoria no banco vinculada ao usuário logado

        return redirect('listar_categorias')
        # após salvar, redireciona para a lista de categorias

    return render(request, 'categorias/criar.html')
    # se não for POST, apenas exibe o formulário