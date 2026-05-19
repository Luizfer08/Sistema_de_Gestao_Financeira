# DATAS E VALORES
from datetime import date
from decimal import Decimal


# RETORNA O PRIMEIRO DIA DO MÊS
def inicio_do_mes(data_ref):

    return date(
        data_ref.year,
        data_ref.month,
        1
    )


# CALCULA QUANTIDADE DE MESES ENTRE DUAS DATAS
def meses_entre(data_inicial, data_final):

    return (

        (data_final.year - data_inicial.year) * 12

        +

        (data_final.month - data_inicial.month)
    )


# VERIFICA SE LANÇAMENTO OCORRE NO MÊS
def ocorre_no_mes(lancamento, data_ref):

    # Mês do lançamento
    mes_lancamento = inicio_do_mes(
        lancamento.data
    )

    # Mês de referência
    mes_referencia = inicio_do_mes(
        data_ref
    )

    # Não exibe lançamentos futuros
    if mes_referencia < mes_lancamento:

        return False

    # LANÇAMENTO RECORRENTE
    # Aparece em todos os meses após criação
    if lancamento.recorrente:

        return True

    # LANÇAMENTO PARCELADO
    if lancamento.parcelada:

        # Quantidade de parcelas
        quantidade = (
            lancamento.quantidade_parcelas or 1
        )

        # Verifica se parcela ainda está ativa
        return (

            meses_entre(
                mes_lancamento,
                mes_referencia
            )

            <

            quantidade
        )

    # LANÇAMENTO NORMAL
    return mes_lancamento == mes_referencia


# FILTRA LANÇAMENTOS DA COMPETÊNCIA
def filtrar_por_competencia(queryset, data_ref):

    return sorted(

        # Filtra apenas lançamentos válidos
        [
            item
            for item in queryset
            if ocorre_no_mes(item, data_ref)
        ],

        # Ordena por data e descrição
        key=lambda item: (
            item.data,
            item.descricao.lower()
        )
    )


# SOMA VALORES DA COMPETÊNCIA
def somar_por_competencia(queryset, data_ref):

    total = Decimal('0')

    # Percorre lançamentos
    for item in queryset:

        # Soma apenas lançamentos válidos
        if ocorre_no_mes(item, data_ref):

            total += item.valor

    return total