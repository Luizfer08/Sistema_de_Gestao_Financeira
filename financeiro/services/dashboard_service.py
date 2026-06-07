# Date e Decimal sao usados nos calculos de meses e valores financeiros.
from datetime import date
from decimal import Decimal

# Funcao central que soma apenas lancamentos validos para a competencia.
from financeiro.competencia import somar_por_competencia

# Models consultados para montar os dados do dashboard.
from financeiro.models import (
    Categoria,
    Despesa,
    Receita
)


# Nomes dos meses exibidos nas telas e nos filtros.
MESES = [
    'Janeiro', 'Fevereiro', 'Marco', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]


# Soma ou subtrai meses mantendo sempre o primeiro dia do mes.
def somar_mes(data_ref, delta):

    mes = data_ref.month + delta
    ano = data_ref.year

    # Ajusta quando o calculo volta para o ano anterior.
    while mes < 1:

        mes += 12
        ano -= 1

    # Ajusta quando o calculo avanca para o proximo ano.
    while mes > 12:

        mes -= 12
        ano += 1

    return date(ano, mes, 1)


# Retorna o ultimo dia do mes recebido.
def fim_do_mes(data_ref):

    proximo_mes = somar_mes(data_ref, 1)

    return date.fromordinal(
        proximo_mes.toordinal() - 1
    )


# Define o mes de referencia vindo da URL ou usa o mes atual.
def obter_mes_referencia(mes=None, ano=None):

    hoje = date.today()

    try:

        # Converte mes e ano recebidos por query string.
        mes = int(mes or hoje.month)
        ano = int(ano or hoje.year)

        return date(ano, mes, 1)

    # Caso a URL venha invalida, volta para o mes atual.
    except ValueError:

        return date(
            hoje.year,
            hoje.month,
            1
        )


# Soma receitas validas para a competencia informada.
def total_receitas_periodo(usuario, data_inicio, data_fim):

    # Busca receitas criadas ate o final do mes.
    receitas = Receita.objects.filter(
        usuario=usuario,
        data__lte=data_fim
    )

    # Aplica regra de receitas fixas, parceladas e comuns.
    return somar_por_competencia(
        receitas,
        data_inicio
    )


# Soma despesas validas para a competencia informada.
def total_despesas_periodo(usuario, data_inicio, data_fim):

    # Busca despesas criadas ate o final do mes.
    despesas = Despesa.objects.filter(
        usuario=usuario,
        data__lte=data_fim
    )

    # Aplica regra de despesas fixas, parceladas e comuns.
    return somar_por_competencia(
        despesas,
        data_inicio
    )


# Calcula saldo previsto de uma competencia.
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


# Calcula percentual de aumento, queda ou estabilidade.
def calcular_variacao(valor_atual, valor_anterior):

    valor_atual = Decimal(valor_atual)
    valor_anterior = Decimal(valor_anterior)

    # Sem valor anterior, qualquer valor positivo representa crescimento.
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

    # Diferenca entre o valor atual e o valor usado para comparacao.
    diferenca = valor_atual - valor_anterior

    percentual = round(
        (abs(diferenca) / abs(valor_anterior)) * 100,
        1
    )

    # Valor atual maior que o anterior.
    if diferenca > 0:

        return {
            'percentual': percentual,
            'direcao': 'up'
        }

    # Valor atual menor que o anterior.
    if diferenca < 0:

        return {
            'percentual': percentual,
            'direcao': 'down'
        }

    # Valores iguais nao geram variacao.
    return {
        'percentual': 0,
        'direcao': 'same'
    }


# Monta os cards principais do dashboard.
def montar_resumo_mensal(usuario, data_ref):

    inicio = data_ref
    fim = fim_do_mes(data_ref)

    # Datas usadas para comparar mes atual, mes anterior e saldo futuro.
    data_anterior = somar_mes(data_ref, -1)
    fim_anterior = fim_do_mes(data_anterior)
    data_futura = somar_mes(data_ref, 1)

    # Totais da competencia selecionada na tela.
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
        data_futura
    )

    # Totais da competencia anterior, usados nas porcentagens.
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
        data_ref
    )

    # Retorna valores e variacoes usados pelos cards do dashboard.
    return {

        'saldo_atual': saldo_atual,
        'saldo_futuro': saldo_futuro,

        'receitas': receitas,
        'despesas': despesas,

        # Percentuais exibidos abaixo dos cards.
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

        # Dados anteriores mantidos para comparacao e depuracao.
        'anterior': {

            'saldo_atual': saldo_anterior,
            'saldo_futuro': saldo_futuro_anterior,

            'receitas': receitas_anterior,
            'despesas': despesas_anterior,
        }
    }


# Monta o historico usado no grafico financeiro.
def montar_historico_financeiro(usuario, data_ref, quantidade=5):

    # Define o primeiro mes que aparecera no grafico.
    inicio = somar_mes(
        data_ref,
        -(quantidade - 1)
    )

    # Cria a sequencia de meses exibida no eixo X.
    meses = [
        somar_mes(inicio, index)
        for index in range(quantidade)
    ]

    return {

        # Labels curtos dos meses.
        'labels': [
            MESES[item.month - 1][:3].upper()
            for item in meses
        ],

        # Valores de receitas por competencia.
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

        # Valores de despesas por competencia.
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

        # Saldo futuro considera sempre o mes seguinte de cada item.
        'saldo_futuro': [
            float(
                calcular_saldo_previsto(
                    usuario,
                    somar_mes(item, 1)
                )
            )
            for item in meses
        ],
    }


# Monta os dados do grafico de categorias.
def montar_categorias(usuario, data_ref):

    inicio = data_ref
    fim = fim_do_mes(data_ref)

    # Busca categorias do usuario logado.
    categorias = Categoria.objects.filter(
        usuario=usuario
    ).order_by('nome')

    dados = []

    for categoria in categorias:

        # Receitas da categoria criadas ate o final do mes.
        receitas = Receita.objects.filter(
            usuario=usuario,
            categoria=categoria,
            data__lte=fim
        )

        # Despesas da categoria criadas ate o final do mes.
        despesas = Despesa.objects.filter(
            usuario=usuario,
            categoria=categoria,
            data__lte=fim
        )

        # Soma receitas e despesas validas para a competencia.
        total = (

            somar_por_competencia(receitas, inicio)

            +

            somar_por_competencia(despesas, inicio)
        )

        # Envia nome, tipo, cor e total para o frontend.
        dados.append({

            'nome': categoria.nome,
            'tipo': categoria.tipo,
            'cor': categoria.cor,
            'total': total,
        })

    return dados


# Monta a lista de ultimas transacoes cadastradas.
def montar_ultimas_transacoes(usuario, limite=5):

    # Busca receitas mais recentes.
    receitas = Receita.objects.filter(
        usuario=usuario
    ).select_related('categoria').order_by('-criado_em')[:limite]

    # Busca despesas mais recentes.
    despesas = Despesa.objects.filter(
        usuario=usuario
    ).select_related('categoria').order_by('-criado_em')[:limite]

    transacoes = []

    # Converte receitas para um formato comum de transacao.
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

    # Converte despesas para o mesmo formato das receitas.
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

    # Mistura receitas e despesas e ordena pela criacao.
    return sorted(
        transacoes,
        key=lambda item: item['criado_em'],
        reverse=True
    )[:limite]


# Gera notificacoes automaticas com base nas variacoes financeiras.
def gerar_notificacoes(usuario, resumo, data_ref):

    notificacoes = []

    # Notifica crescimento de receitas em relacao ao mes anterior.
    if resumo['variacoes']['receitas']['direcao'] == 'up':

        notificacoes.append({
            'tipo': 'receita',
            'texto': (
                f"Receitas aumentaram "
                f"{resumo['variacoes']['receitas']['percentual']}% "
                f"em relacao ao mês anterior."
            )
        })

    # Notifica aumento de despesas em relacao ao mes anterior.
    if resumo['variacoes']['despesas']['direcao'] == 'up':

        notificacoes.append({
            'tipo': 'despesa',
            'texto': (
                f"Despesas aumentaram "
                f"{resumo['variacoes']['despesas']['percentual']}% "
                f"em relacao ao mês anterior."
            )
        })

    # Destaca aumentos expressivos de despesa.
    if (
        resumo['variacoes']['despesas']['direcao'] == 'up'
        and resumo['variacoes']['despesas']['percentual'] >= 30
    ):

        notificacoes.append({
            'tipo': 'despesa',
            'texto': 'Grande aumento nas despesas neste mês.'
        })

    # Alerta quando o saldo atual fica negativo.
    if resumo['saldo_atual'] < 0:

        notificacoes.append({
            'tipo': 'despesa',
            'texto': 'Saldo atual esta negativo neste mês.'
        })

    # Alerta quando a previsao do proximo mes e menor que o saldo atual.
    if resumo['saldo_futuro'] < resumo['saldo_atual']:

        notificacoes.append({
            'tipo': 'despesa',
            'texto': 'Saldo futuro esta abaixo do saldo atual.'
        })

    # Analisa os ultimos tres meses para gerar alertas de tendencia.
    lucros = []
    receitas_3_meses = []
    movimentacoes_3_meses = []

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

        movimentacoes_3_meses.append(
            receitas + despesas
        )

    tem_movimentacao_3_meses = any(
        valor > 0
        for valor in movimentacoes_3_meses
    )

    # Informa quando o mes atual possui maior lucro recente.
    if (
        tem_movimentacao_3_meses
        and len(lucros) == 3
        and lucros[0] == max(lucros)
        and lucros[0] > 0
    ):

        notificacoes.append({
            'tipo': 'receita',
            'texto': 'Maior lucro dos ultimos 3 meses registrado.'
        })

    # Informa quando o mes atual possui menor lucro recente.
    if (
        tem_movimentacao_3_meses
        and len(lucros) == 3
        and lucros[0] == min(lucros)
        and lucros[0] != 0
    ):

        notificacoes.append({
            'tipo': 'despesa',
            'texto': 'Menor lucro registrado nos ultimos 3 meses.'
        })

    # Informa quando receitas ficaram iguais nos ultimos meses.
    if (
        len(receitas_3_meses) == 3
        and tem_movimentacao_3_meses
        and receitas_3_meses[0] > 0
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

    # Compara o saldo futuro com o mes seguinte a ele.
    mes_seguinte = somar_mes(data_ref, 2)

    saldo_proximo = calcular_saldo_previsto(
        usuario,
        mes_seguinte
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
                    f'{crescimento}% para o mês seguinte.'
                )
            })

    return notificacoes[:5]


# Monta todos os blocos usados pela tela do dashboard.
def montar_dashboard(usuario, mes=None, ano=None):

    # Define a competencia selecionada pelo usuario.
    data_ref = obter_mes_referencia(
        mes,
        ano
    )

    # Gera os valores dos cards principais.
    resumo = montar_resumo_mensal(
        usuario,
        data_ref
    )

    # Retorna os dados consumidos pelo template e pelo JavaScript.
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
