from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from financeiro.services.categoria_service import listar_categorias
from financeiro.services.receita_service import (
    criar_receita,
    listar_receitas,
    editar_receita,
    excluir_receita
)


# LISTAR
@login_required
def listar_receitas_view(request):

    receitas = listar_receitas(request.user)
    categorias = listar_categorias(request.user)

    return render(request, 'financeiro/receitas/listar.html', {
        'receitas': receitas,
        'categorias': categorias
    })


# CRIAR
@login_required
def criar_receita_view(request):

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método inválido'})

    try:
        receita = criar_receita(request.user, request.POST)

        return JsonResponse({
            'success': True,
            'id': receita.id,
            'descricao': receita.descricao,
            'valor': float(receita.valor),
            'data': receita.data.strftime('%d/%m/%Y'),
            'categoria': receita.categoria.nome if receita.categoria else "Sem categoria",
            'recorrente': receita.recorrente
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


# EDITAR
@login_required
def editar_receita_view(request, id):

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método inválido'})

    try:
        receita = editar_receita(id, request.user, request.POST)

        return JsonResponse({
            'success': True,
            'descricao': receita.descricao,
            'valor': float(receita.valor)
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


# EXCLUIR
@login_required
def excluir_receita_view(request, id):

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método inválido'})

    try:
        excluir_receita(id, request.user)

        return JsonResponse({
            'success': True
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })