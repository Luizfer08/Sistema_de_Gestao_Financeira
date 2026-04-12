from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from financeiro.services.despesa_service import (
    criar_despesa,
    listar_despesas,
    editar_despesa,
    excluir_despesa
)

from financeiro.services.categoria_service import listar_categorias


# LISTAR
@login_required
def listar_despesas_view(request):

    despesas = listar_despesas(request.user)
    categorias = listar_categorias(request.user)

    return render(request, 'financeiro/despesas/listar.html', {
        'despesas': despesas,
        'categorias': categorias
    })


# CRIAR 
@login_required
def criar_despesa_view(request):

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método inválido'})

    try:
        despesa = criar_despesa(request.user, request.POST)

        return JsonResponse({
            'success': True,
            'id': despesa.id,
            'descricao': despesa.descricao,
            'valor': float(despesa.valor),
            'data': despesa.data.strftime('%d/%m/%Y'),
            'categoria': despesa.categoria.nome if despesa.categoria else "Sem categoria",
            'recorrente': despesa.recorrente
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


# EDITAR 
@login_required
def editar_despesa_view(request, id):

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método inválido'})

    try:
        despesa = editar_despesa(id, request.user, request.POST)

        return JsonResponse({
            'success': True,
            'descricao': despesa.descricao,
            'valor': float(despesa.valor)
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


# EXCLUIR 
@login_required
def excluir_despesa_view(request, id):

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método inválido'})

    try:
        excluir_despesa(id, request.user)

        return JsonResponse({
            'success': True
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })