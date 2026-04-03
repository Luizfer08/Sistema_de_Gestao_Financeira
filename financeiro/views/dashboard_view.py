from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime

# SERVICES
from financeiro.services.receita_service import (
    total_receitas,
    total_receitas_por_data
)

from financeiro.services.despesa_service import (
    total_despesas,
    total_despesas_por_data
)


@login_required
def dashboard(request):

    user = request.user

    receitas_total = total_receitas(user)
    despesas_total = total_despesas(user)

    saldo_atual = receitas_total - despesas_total

    data_param = request.GET.get('data')

    if data_param:
        data_filtro = datetime.strptime(data_param, "%Y-%m-%d").date()
    else:
        data_filtro = datetime.today().date()

    receitas_filtro = total_receitas_por_data(user, data_filtro)
    despesas_filtro = total_despesas_por_data(user, data_filtro)

    saldo_futuro = receitas_filtro - despesas_filtro

    context = {
        'saldo': saldo_atual,
        'receitas': receitas_total,
        'despesas': despesas_total,
        'saldo_futuro': saldo_futuro,
        'data_filtro': data_filtro,
        'receitas_filtro': receitas_filtro,
        'despesas_filtro': despesas_filtro,
    }

    return render(request, 'financeiro/dashboard.html', context)