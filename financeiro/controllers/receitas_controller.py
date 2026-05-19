# DATAS E VALORES
from datetime import date
from decimal import Decimal

# JSON
from django.http import JsonResponse

# RENDER
from django.shortcuts import render

# SEGURANÇA
from django.contrib.auth.decorators import login_required

# SERVICES
from financeiro.services.categoria_service import listar_categorias

from financeiro.services.receita_service import (
    criar_receita,
    listar_receitas_por_periodo,
    total_receitas_por_periodo,
    editar_receita,
    excluir_receita
)


# LISTA DOS MESES
MESES = [
    'Janeiro', 'Fevereiro', 'Marco', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]


# CONVERTE OBJETO RECEITA PARA JSON
def receita_json(receita):

    return {

        # Identificação
        'id': receita.id,

        # Dados principais
        'descricao': receita.descricao,
        'valor': float(receita.valor),

        # Datas formatadas
        'data': receita.data.strftime('%d/%m/%Y'),
        'data_iso': receita.data.strftime('%Y-%m-%d'),

        # Categoria
        'categoria_id': receita.categoria.id if receita.categoria else '',
        'categoria': receita.categoria.nome if receita.categoria else "Sem categoria",
        'categoria_cor': receita.categoria.cor if receita.categoria else "#8FEBDD",

        # Configurações financeiras
        'recorrente': receita.recorrente,
        'parcelada': receita.parcelada,

        # Quantidade de parcelas
        'quantidade_parcelas': receita.quantidade_parcelas or ''
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


# MONTA ALERTA DE VARIAÇÃO DAS RECEITAS
def montar_alerta_receita(total_mes, total_mes_anterior):

    total_atual = Decimal(total_mes or 0)
    total_anterior = Decimal(total_mes_anterior or 0)

    # Não exibe alerta caso os valores sejam iguais
    if total_atual == total_anterior or total_anterior == 0:
        return None

    # Calcula diferença percentual
    diferenca = abs(total_atual - total_anterior)

    percentual = round(
        (diferenca / total_anterior) * 100
    )

    # Alerta de aumento
    if total_atual > total_anterior:

        return {
            'tipo': 'aumento',
            'icone': 'financeiro/img/crescente.png',
            'mensagem': f'A sua receita aumentou {percentual}% em relacao ao mes anterior'
        }

    # Alerta de queda
    return {
        'tipo': 'queda',
        'icone': 'financeiro/img/baixo.png',
        'mensagem': f'A sua receita diminuiu {percentual}% em relacao ao mes anterior'
    }


# LISTAR RECEITAS
@login_required
def listar_receitas_view(request):

    # Define mês atual
    mes_atual = obter_mes_referencia(request)

    # Define mês anterior e próximo
    mes_anterior = somar_mes(mes_atual, -1)
    proximo_mes = somar_mes(mes_atual, 1)

    # Lista receitas do período
    receitas = listar_receitas_por_periodo(
        request.user,
        mes_atual,
        fim_do_mes(mes_atual)
    )

    # Lista categorias de receita
    categorias = listar_categorias(
        request.user,
        'receita'
    )

    # Total de receitas do mês atual
    total_mes = total_receitas_por_periodo(
        request.user,
        mes_atual,
        fim_do_mes(mes_atual)
    )

    # Total do mês anterior
    total_mes_anterior = total_receitas_por_periodo(
        request.user,
        mes_anterior,
        fim_do_mes(mes_anterior)
    )

    # Gera alerta de comparação financeira
    alerta_receita = montar_alerta_receita(
        total_mes,
        total_mes_anterior
    )

    # Renderiza página de receitas
    return render(request, 'financeiro/receitas/listar.html', {

        'receitas': receitas,
        'categorias': categorias,

        # Dados do período atual
        'mes_nome': MESES[mes_atual.month - 1],
        'mes_atual': mes_atual,

        # Navegação entre meses
        'mes_anterior': mes_anterior,
        'proximo_mes': proximo_mes,

        # Dados financeiros
        'total_mes': total_mes,
        'alerta_receita': alerta_receita
    })


# CRIAR RECEITA
@login_required
def criar_receita_view(request):

    # Valida método da requisição
    if request.method != 'POST':

        return JsonResponse({
            'success': False,
            'error': 'Metodo invalido'
        })

    try:

        # Cria receita
        receita = criar_receita(
            request.user,
            request.POST
        )

        # Retorna dados da receita criada
        return JsonResponse({
            'success': True,
            **receita_json(receita)
        })

    # Captura erros
    except Exception as e:

        return JsonResponse({
            'success': False,
            'error': str(e)
        })


# EDITAR RECEITA
@login_required
def editar_receita_view(request, id):

    # Valida método da requisição
    if request.method != 'POST':

        return JsonResponse({
            'success': False,
            'error': 'Metodo invalido'
        })

    try:

        # Atualiza receita
        receita = editar_receita(
            id,
            request.user,
            request.POST
        )

        # Retorna dados atualizados
        return JsonResponse({
            'success': True,
            **receita_json(receita)
        })

    # Captura erros
    except Exception as e:

        return JsonResponse({
            'success': False,
            'error': str(e)
        })


# EXCLUIR RECEITA
@login_required
def excluir_receita_view(request, id):

    # Valida método da requisição
    if request.method != 'POST':

        return JsonResponse({
            'success': False,
            'error': 'Metodo invalido'
        })

    try:

        # Remove receita
        excluir_receita(id, request.user)

        # Retorna sucesso da operação
        return JsonResponse({
            'success': True
        })

    # Captura erros
    except Exception as e:

        return JsonResponse({
            'success': False,
            'error': str(e)
        })