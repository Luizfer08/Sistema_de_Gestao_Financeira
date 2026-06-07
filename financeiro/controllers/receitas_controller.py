# Date e Decimal ajudam no filtro mensal e nos calculos percentuais.
from datetime import date
from decimal import Decimal

# JsonResponse devolve respostas para chamadas AJAX.
from django.http import JsonResponse

# Render devolve a pagina HTML de receitas.
from django.shortcuts import render

# Login_required protege a tela para usuarios autenticados.
from django.contrib.auth.decorators import login_required

# Services usados pela tela de receitas.
from financeiro.services.categoria_service import listar_categorias

from financeiro.services.receita_service import (
    criar_receita,
    listar_receitas_por_periodo,
    total_receitas_por_periodo,
    editar_receita,
    excluir_receita
)


# Nomes dos meses exibidos no filtro mensal.
MESES = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]


# Converte uma receita do banco para o formato JSON usado pelo JavaScript.
def receita_json(receita):

    return {

        # Identificacao do registro.
        'id': receita.id,

        # Dados principais exibidos na tabela.
        'descricao': receita.descricao,
        'valor': float(receita.valor),

        # Datas nos formatos de exibicao e de input HTML.
        'data': receita.data.strftime('%d/%m/%Y'),
        'data_iso': receita.data.strftime('%Y-%m-%d'),

        # Categoria usada na coluna e no ponto colorido.
        'categoria_id': receita.categoria.id if receita.categoria else '',
        'categoria': receita.categoria.nome if receita.categoria else "Sem categoria",
        'categoria_cor': receita.categoria.cor if receita.categoria else "#8FEBDD",

        # Configuracoes de renda fixa e receita parcelada.
        'recorrente': receita.recorrente,
        'parcelada': receita.parcelada,
        'quantidade_parcelas': receita.quantidade_parcelas or ''
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


# Monta o alerta de aumento ou queda das receitas.
def montar_alerta_receita(total_mes, total_mes_anterior):

    total_atual = Decimal(total_mes or 0)
    total_anterior = Decimal(total_mes_anterior or 0)

    # Sem mes anterior nao ha comparacao confiavel.
    if total_atual == total_anterior or total_anterior == 0:
        return None

    diferenca = abs(total_atual - total_anterior)

    percentual = round(
        (diferenca / total_anterior) * 100
    )

    # Mensagem para aumento de receita.
    if total_atual > total_anterior:

        return {
            'tipo': 'aumento',
            'icone': 'financeiro/img/crescente.png',
            'mensagem': f'A sua receita aumentou {percentual}% em relacao ao mes anterior'
        }

    # Mensagem para queda de receita.
    return {
        'tipo': 'queda',
        'icone': 'financeiro/img/baixo.png',
        'mensagem': f'A sua receita diminuiu {percentual}% em relacao ao mes anterior'
    }


# Renderiza a tela de receitas do mes selecionado.
@login_required
def listar_receitas_view(request):

    # Competencia atual da tela.
    mes_atual = obter_mes_referencia(request)

    # Links de navegacao mensal.
    mes_anterior = somar_mes(mes_atual, -1)
    proximo_mes = somar_mes(mes_atual, 1)

    # Receitas validas para a competencia.
    receitas = listar_receitas_por_periodo(
        request.user,
        mes_atual,
        fim_do_mes(mes_atual)
    )

    # Apenas categorias de receita sao listadas no popup de receita.
    categorias = listar_categorias(
        request.user,
        'receita'
    )

    # Total do mes atual.
    total_mes = total_receitas_por_periodo(
        request.user,
        mes_atual,
        fim_do_mes(mes_atual)
    )

    # Total do mes anterior para gerar alerta percentual.
    total_mes_anterior = total_receitas_por_periodo(
        request.user,
        mes_anterior,
        fim_do_mes(mes_anterior)
    )

    alerta_receita = montar_alerta_receita(
        total_mes,
        total_mes_anterior
    )

    return render(request, 'financeiro/receitas/listar.html', {

        'receitas': receitas,
        'categorias': categorias,
        'mes_nome': MESES[mes_atual.month - 1],
        'mes_atual': mes_atual,
        'mes_anterior': mes_anterior,
        'proximo_mes': proximo_mes,
        'total_mes': total_mes,
        'alerta_receita': alerta_receita
    })


# Cria uma receita por requisicao AJAX.
@login_required
def criar_receita_view(request):

    # Criacao deve acontecer apenas por POST.
    if request.method != 'POST':

        return JsonResponse({
            'success': False,
            'error': 'Metodo invalido'
        })

    try:

        receita = criar_receita(
            request.user,
            request.POST
        )

        return JsonResponse({
            'success': True,
            **receita_json(receita)
        })

    except Exception as e:

        return JsonResponse({
            'success': False,
            'error': str(e)
        })


# Edita uma receita por requisicao AJAX.
@login_required
def editar_receita_view(request, id):

    # Edicao deve acontecer apenas por POST.
    if request.method != 'POST':

        return JsonResponse({
            'success': False,
            'error': 'Metodo invalido'
        })

    try:

        receita = editar_receita(
            id,
            request.user,
            request.POST
        )

        return JsonResponse({
            'success': True,
            **receita_json(receita)
        })

    except Exception as e:

        return JsonResponse({
            'success': False,
            'error': str(e)
        })


# Exclui uma receita por requisicao AJAX.
@login_required
def excluir_receita_view(request, id):

    # Exclusao deve acontecer apenas por POST.
    if request.method != 'POST':

        return JsonResponse({
            'success': False,
            'error': 'Metodo invalido'
        })

    try:

        excluir_receita(id, request.user)

        return JsonResponse({
            'success': True
        })

    except Exception as e:

        return JsonResponse({
            'success': False,
            'error': str(e)
        })
