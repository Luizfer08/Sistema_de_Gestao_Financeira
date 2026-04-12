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


@login_required
def listar_despesas_view(request):

    despesas = listar_despesas(request.user)
    categorias = listar_categorias(request.user)

    return render(request, 'financeiro/despesas/listar.html', {
        'despesas': despesas,
        'categorias': categorias
    })


@login_required
def criar_despesa_view(request):

    if request.method == 'POST':
        try:
            despesa = criar_despesa(request.user, request.POST)

            return JsonResponse({
                'success': True,
                'id': despesa.id
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False})


@login_required
def editar_despesa_view(request, id):

    if request.method == 'POST':
        try:
            despesa = editar_despesa(id, request.user, request.POST)

            return JsonResponse({
                'success': True,
                'descricao': despesa.descricao,
                'valor': float(despesa.valor)
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False})


@login_required
def excluir_despesa_view(request, id):

    if request.method == 'POST':
        try:
            excluir_despesa(id, request.user)
            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False})