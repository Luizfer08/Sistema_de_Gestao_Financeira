# Date cria datas normalizadas para o primeiro dia de cada mes.
from datetime import date

# Decimal evita perda de precisao em calculos financeiros.
from decimal import Decimal


# Retorna o primeiro dia do mes usado como competencia financeira.
def inicio_do_mes(data_ref):

    return date(
        data_ref.year,
        data_ref.month,
        1
    )


# Calcula a distancia em meses entre duas competencias.
def meses_entre(data_inicial, data_final):

    return (

        (data_final.year - data_inicial.year) * 12

        +

        (data_final.month - data_inicial.month)
    )


# Verifica se uma receita ou despesa deve aparecer no mes informado.
def ocorre_no_mes(lancamento, data_ref):

    # Normaliza a data original do lancamento para o inicio do mes.
    mes_lancamento = inicio_do_mes(
        lancamento.data
    )

    # Normaliza a data selecionada na tela para o inicio do mes.
    mes_referencia = inicio_do_mes(
        data_ref
    )

    # Lancamentos cadastrados no futuro nao entram em meses anteriores.
    if mes_referencia < mes_lancamento:

        return False

    # Lancamento fixo entra em todos os meses a partir do cadastro.
    if lancamento.recorrente:

        return True

    # Lancamento parcelado entra somente enquanto houver parcela ativa.
    if lancamento.parcelada:

        # Caso a quantidade nao esteja preenchida, considera uma parcela.
        quantidade = (
            lancamento.quantidade_parcelas or 1
        )

        # Exemplo: 2 parcelas em maio entram em maio e junho.
        return (

            meses_entre(
                mes_lancamento,
                mes_referencia
            )

            <

            quantidade
        )

    # Lancamento comum entra apenas no mes em que foi cadastrado.
    return mes_lancamento == mes_referencia


# Filtra e ordena lancamentos validos para uma competencia.
def filtrar_por_competencia(queryset, data_ref):

    return sorted(

        # Mantem apenas itens que pertencem ao mes selecionado.
        [
            item
            for item in queryset
            if ocorre_no_mes(item, data_ref)
        ],

        # Ordena por data e descricao para exibir a tabela de forma previsivel.
        key=lambda item: (
            item.data,
            item.descricao.lower()
        )
    )


# Soma os valores dos lancamentos que pertencem a competencia informada.
def somar_por_competencia(queryset, data_ref):

    total = Decimal('0')

    # Percorre receitas ou despesas recebidas do banco.
    for item in queryset:

        # Soma somente itens validos para o mes selecionado.
        if ocorre_no_mes(item, data_ref):

            total += item.valor

    return total
