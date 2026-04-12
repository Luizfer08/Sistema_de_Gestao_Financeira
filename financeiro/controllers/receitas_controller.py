from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from financeiro.services.categoria_service import listar_categorias
from financeiro.services.receita_service import (
    criar_receita,
    listar_receitas,
    editar_receita,
    excluir_receita
)

from financeiro.models import Categoria


@login_required
def listar_receitas_view(request):

    receitas = listar_receitas(request.user)
    categorias = listar_categorias(request.user)

    return render(request, 'financeiro/receitas/listar.html', {
        'receitas': receitas,
        'categorias': categorias
    })

@login_required
def criar_receita_view(request):

    if request.method == 'POST':
        try:
            receita = criar_receita(request.user, request.POST)

            return JsonResponse({
                'success': True,
                'id': receita.id,
                'descricao': receita.descricao,
                'valor': float(receita.valor),
                'data': receita.data.strftime('%d/%m/%Y')
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False})

@login_required
def editar_receita_view(request, id):

    if request.method == 'POST':
        try:
            receita = editar_receita(id, request.user, request.POST)

            return JsonResponse({
                'success': True,
                'descricao': receita.descricao,
                'valor': float(receita.valor)
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False})


@login_required
def excluir_receita_view(request, id):

    if request.method == 'POST':
        try:
            excluir_receita(id, request.user)

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False})