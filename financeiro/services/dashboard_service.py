from datetime import date, timedelta
from django.db.models import Sum

from financeiro.models import Receita, Despesa

from datetime import date


# SALDO ATUAL
def calcular_saldo_atual(usuario):

    total_receitas = Receita.objects.filter(
        usuario=usuario
    ).aggregate(total=Sum('valor'))['total'] or 0

    total_despesas = Despesa.objects.filter(
        usuario=usuario
    ).aggregate(total=Sum('valor'))['total'] or 0

    return total_receitas - total_despesas


# RESUMO GERAL
def calcular_resumo(usuario):

    total_receitas = Receita.objects.filter(
        usuario=usuario
    ).aggregate(total=Sum('valor'))['total'] or 0

    total_despesas = Despesa.objects.filter(
        usuario=usuario
    ).aggregate(total=Sum('valor'))['total'] or 0

    saldo = total_receitas - total_despesas

    return total_receitas, total_despesas, saldo


# PREVISÃO MENSAL 
def calcular_saldo_previsto(usuario, mes, ano):

    data_referencia = date(ano, mes, 1)

    receitas = Receita.objects.filter(usuario=usuario)
    despesas = Despesa.objects.filter(usuario=usuario)

    total_receitas = 0
    total_despesas = 0

    # RECEITAS
    for receita in receitas:

        if receita.recorrente:
            if receita.is_ativa_em(data_referencia):
                total_receitas += float(receita.valor)

        else:
            if receita.data.month == mes and receita.data.year == ano:
                total_receitas += float(receita.valor)

    # DESPESAS
    for despesa in despesas:

        if despesa.recorrente:
            if despesa.is_ativa_em(data_referencia):
                total_despesas += float(despesa.valor)

        else:
            if despesa.data.month == mes and despesa.data.year == ano:
                total_despesas += float(despesa.valor)

    return total_receitas - total_despesas


# ALERTAS INTELIGENTES
def gerar_alertas(usuario, mes, ano):

    total_receitas, total_despesas, saldo = calcular_resumo(usuario)
    saldo_previsto = calcular_saldo_previsto(usuario, mes, ano)

    alertas_gerais = []
    alerta_previsto = None

    # ALERTAS GERAIS
    if saldo < 0:
        alertas_gerais.append("Seu saldo atual está negativo")

    if total_receitas > 0:
        percentual = (total_despesas / total_receitas) * 100

        if percentual >= 90:
            alertas_gerais.append("Você já gastou mais de 90% da sua renda")
        elif percentual >= 70:
            alertas_gerais.append("Seus gastos estão altos")

    # ALERTA DO PREVISTO
    if saldo_previsto < 0:
        alerta_previsto = "Seu saldo previsto para este mês será negativo"

    return alertas_gerais, alerta_previsto