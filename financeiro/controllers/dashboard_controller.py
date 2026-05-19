# SEGURANÇA
from django.contrib.auth.decorators import login_required

# JSON
from django.http import JsonResponse

# RENDER
from django.shortcuts import render

# SERVICES
from financeiro.services.dashboard_service import montar_dashboard


# DASHBOARD PRINCIPAL
@login_required
def dashboard(request):

    # Monta dados do dashboard com base no usuário e período selecionado
    dados = montar_dashboard(
        request.user,
        request.GET.get('mes'),
        request.GET.get('ano')
    )

    # Renderiza página do dashboard
    return render(
        request,
        'financeiro/dashboard.html',
        dados
    )


# API DE DADOS DO DASHBOARD
@login_required
def dashboard_dados(request):

    # Obtém dados atualizados do dashboard
    dados = montar_dashboard(
        request.user,
        request.GET.get('mes'),
        request.GET.get('ano')
    )

    # Resumo financeiro
    resumo = dados['resumo']

    # Retorna dados em formato JSON
    return JsonResponse({

        # Valores financeiros
        'saldo_atual': float(resumo['saldo_atual']),
        'saldo_futuro': float(resumo['saldo_futuro']),
        'receitas': float(resumo['receitas']),
        'despesas': float(resumo['despesas']),

        # Dados de variação percentual
        'variacoes': resumo['variacoes'],

        # Lista de notificações
        'notificacoes': dados['notificacoes'],

        # Dados do gráfico financeiro
        'grafico_financeiro': dados['grafico_financeiro'],

        # Dados das categorias
        'categorias': [
            {
                'nome': item['nome'],
                'tipo': item['tipo'],
                'cor': item['cor'],
                'total': float(item['total']),
            }

            # Percorre categorias retornadas pelo service
            for item in dados['categorias']
        ],

        # Mês e ano atual selecionado
        'mes': dados['mes_atual'].month,
        'ano': dados['mes_atual'].year,
    })