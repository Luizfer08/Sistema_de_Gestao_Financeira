# RENDER
from django.shortcuts import render

# SEGURANÇA
from django.contrib.auth.decorators import login_required

# JSON
from django.http import JsonResponse

# DATAS E VALORES
from datetime import date
from decimal import Decimal

# SERVICES
from financeiro.services.despesa_service import (
    criar_despesa,
    listar_despesas_por_periodo,
    total_despesas_por_periodo,
    editar_despesa,
    excluir_despesa
)

from financeiro.services.categoria_service import listar_categorias


# LISTA DOS MESES
MESES = [
    'Janeiro', 'Fevereiro', 'Marco', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]


# CONVERTE OBJETO DESPESA PARA JSON
def despesa_json(despesa):

    return {

        # Identificação
        'id': despesa.id,

        # Dados principais
        'descricao': despesa.descricao,
        'valor': float(despesa.valor),

        # Datas formatadas
        'data': despesa.data.strftime('%d/%m/%Y'),
        'data_iso': despesa.data.strftime('%Y-%m-%d'),

        # Categoria
        'categoria_id': despesa.categoria.id if despesa.categoria else '',
        'categoria': despesa.categoria.nome if despesa.categoria else "Sem categoria",
        'categoria_cor': despesa.categoria.cor if despesa.categoria else "#8FEBDD",

        # Conta vinculada
        'conta': despesa.conta,

        # Configurações financeiras
        'recorrente': despesa.recorrente,
        'parcelada': despesa.parcelada,

        # Quantidade de parcelas
        'quantidade_parcelas': despesa.quantidade_parcelas or ''
    }


# OBTÉM MÊS E ANO DA URL
def obter_mes_referencia(request):

    hoje = date.today()

    try:

        # Obtém mês e ano enviados pela URL
        ano = int(request.GET.get('ano', hoje.year))
        mes = int(request.GET.get('mes', hoje.month))

        return date(ano, mes, 1)

    # Caso valor inválido retorna mês atual
    except ValueError:
        return date(hoje.year, hoje.month, 1)


# SOMA OU SUBTRAI MESES
def somar_mes(data_ref, delta):

    mes = data_ref.month + delta
    ano = data_ref.year

    # Ajusta mês anterior
    while mes < 1:
        mes += 12
        ano -= 1

    # Ajusta próximo mês
    while mes > 12:
        mes -= 12
        ano += 1

    return date(ano, mes, 1)


# RETORNA ÚLTIMO DIA DO MÊS
def fim_do_mes(data_ref):

    proximo_mes = somar_mes(data_ref, 1)

    return date.fromordinal(
        proximo_mes.toordinal() - 1
    )


# LISTAR DESPESAS
@login_required
def listar_despesas_view(request):

    # Define mês atual selecionado
    mes_atual = obter_mes_referencia(request)

    # Define mês anterior e próximo
    mes_anterior = somar_mes(mes_atual, -1)
    proximo_mes = somar_mes(mes_atual, 1)

    # Lista despesas do período
    despesas = listar_despesas_por_periodo(
        request.user,
        mes_atual,
        fim_do_mes(mes_atual)
    )

    # Lista categorias de despesa
    categorias = listar_categorias(
        request.user,
        'despesa'
    )

    # Total do mês atual
    total_mes = total_despesas_por_periodo(
        request.user,
        mes_atual,
        fim_do_mes(mes_atual)
    )

    # Total do mês anterior
    total_mes_anterior = total_despesas_por_periodo(
        request.user,
        mes_anterior,
        fim_do_mes(mes_anterior)
    )

    # Percentual de aumento das despesas
    percentual_alerta = None

    if total_mes_anterior and total_mes > total_mes_anterior:

        diferenca = Decimal(total_mes) - Decimal(total_mes_anterior)

        percentual_alerta = round(
            (diferenca / Decimal(total_mes_anterior)) * 100
        )

    # Renderiza página
    return render(request, 'financeiro/despesas/listar.html', {

        'despesas': despesas,
        'categorias': categorias,

        # Nome do mês atual
        'mes_nome': MESES[mes_atual.month - 1],

        # Dados de navegação
        'mes_atual': mes_atual,
        'mes_anterior': mes_anterior,
        'proximo_mes': proximo_mes,

        # Dados financeiros
        'total_mes': total_mes,
        'percentual_alerta': percentual_alerta
    })


# CRIAR DESPESA
@login_required
def criar_despesa_view(request):

    # Valida método da requisição
    if request.method != 'POST':

        return JsonResponse({
            'success': False,
            'error': 'Método inválido'
        })

    try:

        # Cria despesa
        despesa = criar_despesa(
            request.user,
            request.POST
        )

        # Retorna dados da despesa criada
        return JsonResponse({
            'success': True,
            **despesa_json(despesa)
        })

    # Captura erros
    except Exception as e:

        return JsonResponse({
            'success': False,
            'error': str(e)
        })


# EDITAR DESPESA
@login_required
def editar_despesa_view(request, id):

    # Valida método da requisição
    if request.method != 'POST':

        return JsonResponse({
            'success': False,
            'error': 'Método inválido'
        })

    try:

        # Atualiza despesa
        despesa = editar_despesa(
            id,
            request.user,
            request.POST
        )

        # Retorna dados atualizados
        return JsonResponse({
            'success': True,
            **despesa_json(despesa)
        })

    # Captura erros
    except Exception as e:

        return JsonResponse({
            'success': False,
            'error': str(e)
        })


# EXCLUIR DESPESA
@login_required
def excluir_despesa_view(request, id):

    # Valida método da requisição
    if request.method != 'POST':

        return JsonResponse({
            'success': False,
            'error': 'Método inválido'
        })

    try:

        # Remove despesa
        excluir_despesa(id, request.user)

        # Retorna sucesso
        return JsonResponse({
            'success': True
        })

    # Captura erros
    except Exception as e:

        return JsonResponse({
            'success': False,
            'error': str(e)
        })