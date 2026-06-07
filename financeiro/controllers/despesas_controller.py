# Date e Decimal ajudam no filtro mensal e nos calculos percentuais.
from datetime import date
from decimal import Decimal

# Render devolve a pagina HTML de despesas.
from django.shortcuts import render

# Login_required protege a tela para usuarios autenticados.
from django.contrib.auth.decorators import login_required

# JsonResponse devolve respostas para chamadas AJAX.
from django.http import JsonResponse

# Services usados pela tela de despesas.
from financeiro.services.despesa_service import (
    criar_despesa,
    listar_despesas_por_periodo,
    total_despesas_por_periodo,
    editar_despesa,
    excluir_despesa
)

from financeiro.services.categoria_service import listar_categorias


# Nomes dos meses exibidos no filtro mensal.
MESES = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]


# Converte uma despesa do banco para o formato JSON usado pelo JavaScript.
def despesa_json(despesa):

    return {

        # Identificacao do registro.
        'id': despesa.id,

        # Dados principais exibidos na tabela.
        'descricao': despesa.descricao,
        'valor': float(despesa.valor),

        # Datas nos formatos de exibicao e de input HTML.
        'data': despesa.data.strftime('%d/%m/%Y'),
        'data_iso': despesa.data.strftime('%Y-%m-%d'),

        # Categoria usada na coluna e no ponto colorido.
        'categoria_id': despesa.categoria.id if despesa.categoria else '',
        'categoria': despesa.categoria.nome if despesa.categoria else "Sem categoria",
        'categoria_cor': despesa.categoria.cor if despesa.categoria else "#8FEBDD",

        # Conta e exibida apenas nas despesas.
        'conta': despesa.conta,

        # Configuracoes de despesa fixa e despesa parcelada.
        'recorrente': despesa.recorrente,
        'parcelada': despesa.parcelada,
        'quantidade_parcelas': despesa.quantidade_parcelas or ''
    }


# Obtem o mes e ano selecionados na URL.
def obter_mes_referencia(request):

    hoje = date.today()

    try:

        ano = int(request.GET.get('ano', hoje.year))
        mes = int(request.GET.get('mes', hoje.month))

        return date(ano, mes, 1)

    except ValueError:
        return date(hoje.year, hoje.month, 1)


# Soma ou subtrai meses mantendo o primeiro dia.
def somar_mes(data_ref, delta):

    mes = data_ref.month + delta
    ano = data_ref.year

    # Ajusta quando volta para o ano anterior.
    while mes < 1:
        mes += 12
        ano -= 1

    # Ajusta quando avanca para o proximo ano.
    while mes > 12:
        mes -= 12
        ano += 1

    return date(ano, mes, 1)


# Retorna o ultimo dia do mes selecionado.
def fim_do_mes(data_ref):

    proximo_mes = somar_mes(data_ref, 1)

    return date.fromordinal(
        proximo_mes.toordinal() - 1
    )


# Renderiza a tela de despesas do mes selecionado.
@login_required
def listar_despesas_view(request):

    # Competencia atual da tela.
    mes_atual = obter_mes_referencia(request)

    # Links de navegacao mensal.
    mes_anterior = somar_mes(mes_atual, -1)
    proximo_mes = somar_mes(mes_atual, 1)

    # Despesas validas para a competencia.
    despesas = listar_despesas_por_periodo(
        request.user,
        mes_atual,
        fim_do_mes(mes_atual)
    )

    # Apenas categorias de despesa sao listadas no popup de despesa.
    categorias = listar_categorias(
        request.user,
        'despesa'
    )

    # Total do mes atual.
    total_mes = total_despesas_por_periodo(
        request.user,
        mes_atual,
        fim_do_mes(mes_atual)
    )

    # Total do mes anterior para gerar alerta percentual.
    total_mes_anterior = total_despesas_por_periodo(
        request.user,
        mes_anterior,
        fim_do_mes(mes_anterior)
    )

    # Alerta aparece apenas quando a despesa aumenta.
    percentual_alerta = None

    if total_mes_anterior and total_mes > total_mes_anterior:

        diferenca = Decimal(total_mes) - Decimal(total_mes_anterior)

        percentual_alerta = round(
            (diferenca / Decimal(total_mes_anterior)) * 100
        )

    return render(request, 'financeiro/despesas/listar.html', {

        'despesas': despesas,
        'categorias': categorias,
        'mes_nome': MESES[mes_atual.month - 1],
        'mes_atual': mes_atual,
        'mes_anterior': mes_anterior,
        'proximo_mes': proximo_mes,
        'total_mes': total_mes,
        'percentual_alerta': percentual_alerta
    })


# Cria uma despesa por requisicao AJAX.
@login_required
def criar_despesa_view(request):

    # Criacao deve acontecer apenas por POST.
    if request.method != 'POST':

        return JsonResponse({
            'success': False,
            'error': 'Metodo invalido'
        })

    try:

        despesa = criar_despesa(
            request.user,
            request.POST
        )

        return JsonResponse({
            'success': True,
            **despesa_json(despesa)
        })

    except Exception as e:

        return JsonResponse({
            'success': False,
            'error': str(e)
        })


# Edita uma despesa por requisicao AJAX.
@login_required
def editar_despesa_view(request, id):

    # Edicao deve acontecer apenas por POST.
    if request.method != 'POST':

        return JsonResponse({
            'success': False,
            'error': 'Metodo invalido'
        })

    try:

        despesa = editar_despesa(
            id,
            request.user,
            request.POST
        )

        return JsonResponse({
            'success': True,
            **despesa_json(despesa)
        })

    except Exception as e:

        return JsonResponse({
            'success': False,
            'error': str(e)
        })


# Exclui uma despesa por requisicao AJAX.
@login_required
def excluir_despesa_view(request, id):

    # Exclusao deve acontecer apenas por POST.
    if request.method != 'POST':

        return JsonResponse({
            'success': False,
            'error': 'Metodo invalido'
        })

    try:

        excluir_despesa(id, request.user)

        return JsonResponse({
            'success': True
        })

    except Exception as e:

        return JsonResponse({
            'success': False,
            'error': str(e)
        })
