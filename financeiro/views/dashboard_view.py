# Renderização de templates HTML
from django.shortcuts import render

# Proteção de rota (somente usuário logado)
from django.contrib.auth.decorators import login_required

# Retorno JSON (para requisições AJAX)
from django.http import JsonResponse

# Manipulação de datas
from datetime import datetime

from financeiro.services.receita_service import (
    total_receitas,
    total_receitas_por_data
)

from financeiro.services.despesa_service import (
    total_despesas,
    total_despesas_por_data
)

def obter_data_filtro(request):
    """
    Centraliza a lógica de captura e validação da data.
    Evita duplicação de código entre as views.
    """
    data_param = request.GET.get('data')

    if data_param:
        try:
            return datetime.strptime(data_param, "%Y-%m-%d").date()
        except ValueError:
            pass

    return datetime.today().date()


@login_required
def dashboard(request):

    user = request.user

    receitas_total = total_receitas(user)
    despesas_total = total_despesas(user)

    saldo_atual = receitas_total - despesas_total

    data_filtro = obter_data_filtro(request)

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

@login_required
def dashboard_dados(request):

    user = request.user

    data_filtro = obter_data_filtro(request)

    receitas = total_receitas_por_data(user, data_filtro)
    despesas = total_despesas_por_data(user, data_filtro)

    saldo = receitas - despesas

    return JsonResponse({
        'receitas': float(receitas),
        'despesas': float(despesas),
        'saldo': float(saldo),
        'data': data_filtro.strftime("%d/%m/%Y")
    })