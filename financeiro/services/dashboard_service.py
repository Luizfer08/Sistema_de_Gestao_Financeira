# DATAS E VALORES
from datetime import date
from decimal import Decimal

# COMPETÊNCIA FINANCEIRA
from financeiro.competencia import somar_por_competencia

# MODELS
from financeiro.models import (
    Categoria,
    Despesa,
    Receita
)


# LISTA DOS MESES
MESES = [
    'Janeiro', 'Fevereiro', 'Marco', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]


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


# OBTÉM MÊS DE REFERÊNCIA
def obter_mes_referencia(mes=None, ano=None):

    hoje = date.today()

    try:

        # Define mês e ano recebidos
        mes = int(mes or hoje.month)
        ano = int(ano or hoje.year)

        return date(ano, mes, 1)

    # Caso valor inválido retorna mês atual
    except ValueError:

        return date(
            hoje.year,
            hoje.month,
            1
        )


# TOTAL DE RECEITAS DO PERÍODO
def total_receitas_periodo(usuario, data_inicio, data_fim):

    # Busca receitas até data final
    receitas = Receita.objects.filter(
        usuario=usuario,
        data__lte=data_fim
    )

    # Soma receitas válidas da competência
    return somar_por_competencia(
        receitas,
        data_inicio
    )


# TOTAL DE DESPESAS DO PERÍODO
def total_despesas_periodo(usuario, data_inicio, data_fim):

    # Busca despesas até data final
    despesas = Despesa.objects.filter(
        usuario=usuario,
        data__lte=data_fim
    )

    # Soma despesas válidas da competência
    return somar_por_competencia(
        despesas,
        data_inicio
    )


# CALCULA SALDO PREVISTO
def calcular_saldo_previsto(usuario, data_ref):

    return (

        total_receitas_periodo(
            usuario,
            data_ref,
            fim_do_mes(data_ref)
        )

        -

        total_despesas_periodo(
            usuario,
            data_ref,
            fim_do_mes(data_ref)
        )
    )


# CALCULA VARIAÇÃO PERCENTUAL
def calcular_variacao(valor_atual, valor_anterior):

    valor_atual = Decimal(valor_atual)
    valor_anterior = Decimal(valor_anterior)

    # Caso não exista valor anterior
    if valor_anterior == 0:

        if valor_atual > 0:

            return {
                'percentual': 100,
                'direcao': 'up'
            }

        return {
            'percentual': 0,
            'direcao': 'same'
        }

    # Calcula diferença
    diferenca = valor_atual - valor_anterior

    percentual = round(
        (abs(diferenca) / abs(valor_anterior)) * 100,
        1
    )

    # Variação positiva
    if diferenca > 0:

        return {
            'percentual': percentual,
            'direcao': 'up'
        }

    # Variação negativa
    if diferenca < 0:

        return {
            'percentual': percentual,
            'direcao': 'down'
        }

    # Sem alteração
    return {
        'percentual': 0,
        'direcao': 'same'
    }


# MONTA RESUMO MENSAL
def montar_resumo_mensal(usuario, data_ref):

    inicio = data_ref
    fim = fim_do_mes(data_ref)

    # Define mês anterior
    data_anterior = somar_mes(data_ref, -1)
    fim_anterior = fim_do_mes(data_anterior)

    # Totais do mês atual
    receitas = total_receitas_periodo(
        usuario,
        inicio,
        fim
    )

    despesas = total_despesas_periodo(
        usuario,
        inicio,
        fim
    )

    saldo_atual = receitas - despesas

    saldo_futuro = calcular_saldo_previsto(
        usuario,
        data_ref
    )

    # Totais do mês anterior
    receitas_anterior = total_receitas_periodo(
        usuario,
        data_anterior,
        fim_anterior
    )

    despesas_anterior = total_despesas_periodo(
        usuario,
        data_anterior,
        fim_anterior
    )

    saldo_anterior = receitas_anterior - despesas_anterior

    saldo_futuro_anterior = calcular_saldo_previsto(
        usuario,
        data_anterior
    )

    # Retorna resumo financeiro
    return {

        'saldo_atual': saldo_atual,
        'saldo_futuro': saldo_futuro,

        'receitas': receitas,
        'despesas': despesas,

        # Variações percentuais
        'variacoes': {

            'saldo_atual': calcular_variacao(
                saldo_atual,
                saldo_anterior
            ),

            'saldo_futuro': calcular_variacao(
                saldo_futuro,
                saldo_futuro_anterior
            ),

            'receitas': calcular_variacao(
                receitas,
                receitas_anterior
            ),

            'despesas': calcular_variacao(
                despesas,
                despesas_anterior
            ),
        },

        # Dados do mês anterior
        'anterior': {

            'saldo_atual': saldo_anterior,
            'saldo_futuro': saldo_futuro_anterior,

            'receitas': receitas_anterior,
            'despesas': despesas_anterior,
        }
    }


# MONTA HISTÓRICO FINANCEIRO
def montar_historico_financeiro(usuario, data_ref, quantidade=5):

    # Define primeiro mês do histórico
    inicio = somar_mes(
        data_ref,
        -(quantidade - 1)
    )

    # Lista meses do período
    meses = [
        somar_mes(inicio, index)
        for index in range(quantidade)
    ]

    return {

        # Labels do gráfico
        'labels': [
            MESES[item.month - 1][:3].upper()
            for item in meses
        ],

        # Valores de receitas
        'receitas': [
            float(
                total_receitas_periodo(
                    usuario,
                    item,
                    fim_do_mes(item)
                )
            )
            for item in meses
        ],

        # Valores de despesas
        'despesas': [
            float(
                total_despesas_periodo(
                    usuario,
                    item,
                    fim_do_mes(item)
                )
            )
            for item in meses
        ],

        # Valores do saldo futuro
        'saldo_futuro': [
            float(
                calcular_saldo_previsto(
                    usuario,
                    item
                )
            )
            for item in meses
        ],
    }


# MONTA DADOS DAS CATEGORIAS
def montar_categorias(usuario, data_ref):

    inicio = data_ref
    fim = fim_do_mes(data_ref)

    # Busca categorias do usuário
    categorias = Categoria.objects.filter(
        usuario=usuario
    ).order_by('nome')

    dados = []

    for categoria in categorias:

        # Busca receitas da categoria
        receitas = Receita.objects.filter(
            usuario=usuario,
            categoria=categoria,
            data__lte=fim
        )

        # Busca despesas da categoria
        despesas = Despesa.objects.filter(
            usuario=usuario,
            categoria=categoria,
            data__lte=fim
        )

        # Soma movimentações da categoria
        total = (

            somar_por_competencia(receitas, inicio)

            +

            somar_por_competencia(despesas, inicio)
        )

        # Adiciona categoria aos dados
        dados.append({

            'nome': categoria.nome,
            'tipo': categoria.tipo,
            'cor': categoria.cor,
            'total': total,
        })

    return dados


# MONTA ÚLTIMAS TRANSAÇÕES
def montar_ultimas_transacoes(usuario, limite=5):

    # Busca últimas receitas
    receitas = Receita.objects.filter(
        usuario=usuario
    ).select_related('categoria').order_by('-criado_em')[:limite]

    # Busca últimas despesas
    despesas = Despesa.objects.filter(
        usuario=usuario
    ).select_related('categoria').order_by('-criado_em')[:limite]

    transacoes = []

    # Adiciona receitas
    for receita in receitas:

        transacoes.append({

            'tipo': 'receita',

            'descricao': receita.descricao,

            'categoria': (
                receita.categoria.nome
                if receita.categoria
                else 'Sem categoria'
            ),

            'data': receita.data,
            'valor': receita.valor,

            'criado_em': receita.criado_em,
        })

    # Adiciona despesas
    for despesa in despesas:

        transacoes.append({

            'tipo': 'despesa',

            'descricao': despesa.descricao,

            'categoria': (
                despesa.categoria.nome
                if despesa.categoria
                else 'Sem categoria'
            ),

            'data': despesa.data,
            'valor': despesa.valor,

            'criado_em': despesa.criado_em,
        })

    # Ordena transações pela data de criação
    return sorted(
        transacoes,
        key=lambda item: item['criado_em'],
        reverse=True
    )[:limite]


# GERA NOTIFICAÇÕES DO DASHBOARD
def gerar_notificacoes(usuario, resumo, data_ref):

    notificacoes = []

    # RECEITAS AUMENTARAM
    if resumo['variacoes']['receitas']['direcao'] == 'up':

        notificacoes.append({
            'tipo': 'receita',
            'texto': (
                f"Receitas aumentaram "
                f"{resumo['variacoes']['receitas']['percentual']}% "
                f"em relacao ao mês anterior."
            )
        })

    # DESPESAS AUMENTARAM
    if resumo['variacoes']['despesas']['direcao'] == 'up':

        notificacoes.append({
            'tipo': 'despesa',
            'texto': (
                f"Despesas aumentaram "
                f"{resumo['variacoes']['despesas']['percentual']}% "
                f"em relacao ao mês anterior."
            )
        })

    # GRANDE AUMENTO NAS DESPESAS
    if resumo['variacoes']['despesas']['percentual'] >= 30:

        notificacoes.append({
            'tipo': 'despesa',
            'texto': 'Grande aumento nas despesas neste mês.'
        })

    # SALDO NEGATIVO
    if resumo['saldo_atual'] < 0:

        notificacoes.append({
            'tipo': 'despesa',
            'texto': 'Saldo atual esta negativo neste mês.'
        })

    # SALDO FUTURO PIOR
    if resumo['saldo_futuro'] < resumo['saldo_atual']:

        notificacoes.append({
            'tipo': 'despesa',
            'texto': 'Saldo futuro esta abaixo do saldo atual.'
        })

    # ÚLTIMOS 3 MESES
    lucros = []
    receitas_3_meses = []

    for i in range(3):

        mes = somar_mes(data_ref, -i)

        receitas = total_receitas_periodo(
            usuario,
            mes,
            fim_do_mes(mes)
        )

        despesas = total_despesas_periodo(
            usuario,
            mes,
            fim_do_mes(mes)
        )

        lucros.append(receitas - despesas)

        receitas_3_meses.append(receitas)

    # MAIOR LUCRO
    if len(lucros) == 3 and lucros[0] == max(lucros):

        notificacoes.append({
            'tipo': 'receita',
            'texto': 'Maior lucro dos ultimos 3 meses registrado.'
        })

    # MENOR LUCRO
    if len(lucros) == 3 and lucros[0] == min(lucros):

        notificacoes.append({
            'tipo': 'despesa',
            'texto': 'Menor lucro registrado nos ultimos 3 meses.'
        })

    # RECEITAS ESTABILIZADAS
    if (
        len(receitas_3_meses) == 3
        and receitas_3_meses[0] == receitas_3_meses[1]
        and receitas_3_meses[1] == receitas_3_meses[2]
    ):

        notificacoes.append({
            'tipo': 'neutral',
            'texto': (
                'Receitas estabilizadas sem crescimento '
                'nos ultimos 3 meses.'
            )
        })

    # PROJEÇÃO PRÓXIMO MÊS
    proximo_mes = somar_mes(data_ref, 1)

    saldo_proximo = calcular_saldo_previsto(
        usuario,
        proximo_mes
    )

    if resumo['saldo_futuro'] > 0:

        crescimento = round(
            (
                (saldo_proximo - resumo['saldo_futuro'])
                / resumo['saldo_futuro']
            ) * 100,
            1
        )

        if crescimento >= 15:

            notificacoes.append({
                'tipo': 'receita',
                'texto': (
                    f'Projeção indica crescimento de '
                    f'{crescimento}% para o próximo mês.'
                )
            })

    return notificacoes[:5]


# MONTA DASHBOARD COMPLETO
def montar_dashboard(usuario, mes=None, ano=None):

    # Define mês atual
    data_ref = obter_mes_referencia(
        mes,
        ano
    )

    # Gera resumo financeiro
    resumo = montar_resumo_mensal(
        usuario,
        data_ref
    )

    # Retorna todos os dados do dashboard
    return {

        'mes_atual': data_ref,

        'mes_nome': MESES[data_ref.month - 1],

        'mes_anterior': somar_mes(
            data_ref,
            -1
        ),

        'proximo_mes': somar_mes(
            data_ref,
            1
        ),

        'resumo': resumo,

        'notificacoes': gerar_notificacoes(
            usuario,
            resumo,
            data_ref
        ),

        'grafico_financeiro': montar_historico_financeiro(
            usuario,
            data_ref
        ),

        'categorias': montar_categorias(
            usuario,
            data_ref
        ),

        'ultimas_transacoes': montar_ultimas_transacoes(
            usuario
        ),
    }