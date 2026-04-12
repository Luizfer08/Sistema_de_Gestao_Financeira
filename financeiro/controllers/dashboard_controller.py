from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from datetime import date

from financeiro.services.dashboard_service import (
    calcular_resumo,
    calcular_saldo_atual,
    calcular_saldo_previsto,
    gerar_alertas
)


# DASHBOARD
@login_required
def dashboard(request):

    user = request.user
    hoje = date.today()

    # FILTRO MENSAL
    mes = request.GET.get('mes')
    ano = request.GET.get('ano')

    mes = int(mes) if mes else hoje.month
    ano = int(ano) if ano else hoje.year

    # RESUMO GERAL
    receitas_total, despesas_total, saldo_total = calcular_resumo(user)

    # SALDO ATUAL
    saldo_atual = calcular_saldo_atual(user)

    # SALDO PREVISTO
    saldo_previsto = calcular_saldo_previsto(user, mes, ano)

    # ALERTAS (SEPARADOS)
    alertas_gerais, alerta_previsto = gerar_alertas(user, mes, ano)

    context = {
        'saldo_atual': saldo_atual,
        'receitas': receitas_total,
        'despesas': despesas_total,
        'saldo_previsto': saldo_previsto,
        'alertas_gerais': alertas_gerais,
        'alerta_previsto': alerta_previsto,
        'mes': mes,
        'ano': ano,
    }

    return render(request, 'financeiro/dashboard.html', context)


# API (AJAX)
@login_required
def dashboard_dados(request):

    user = request.user
    hoje = date.today()

    mes = request.GET.get('mes')
    ano = request.GET.get('ano')

    mes = int(mes) if mes else hoje.month
    ano = int(ano) if ano else hoje.year

    # RESUMO
    receitas, despesas, saldo = calcular_resumo(user)

    # PREVISÃO
    saldo_previsto = calcular_saldo_previsto(user, mes, ano)

    # ALERTAS
    alertas_gerais, alerta_previsto = gerar_alertas(user, mes, ano)

    return JsonResponse({
        'receitas': float(receitas),
        'despesas': float(despesas),
        'saldo': float(saldo),
        'saldo_previsto': float(saldo_previsto),
        'alertas_gerais': alertas_gerais,
        'alerta_previsto': alerta_previsto,
        'mes': mes,
        'ano': ano
    })