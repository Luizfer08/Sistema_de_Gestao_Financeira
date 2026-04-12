#  RENDER / REDIRECT 
from django.shortcuts import render

#  SEGURANÇA 
from django.contrib.auth.decorators import login_required

#  JSON 
from django.http import JsonResponse

#  SERVICES 
from financeiro.services.categoria_service import (
    criar_categoria,
    listar_categorias,
    editar_categoria,
    excluir_categoria
)


#  LISTAR 
@login_required
def listar_categorias_view(request):

    categorias = listar_categorias(request.user)

    return render(request, 'financeiro/categorias/listar.html', {
        'categorias': categorias
    })


#  CRIAR
@login_required
def criar_categoria_view(request):

    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Método inválido'
        }, status=405)

    try:
        nome = (request.POST.get('nome') or "").strip()

        if not nome:
            return JsonResponse({
                'success': False,
                'error': 'Nome obrigatório'
            })

        categoria = criar_categoria(request.user, nome)

        return JsonResponse({
            'success': True,
            'id': categoria.id,
            'nome': categoria.nome
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


#  EDITAR
@login_required
def editar_categoria_view(request, id):

    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Método inválido'
        }, status=405)

    try:
        nome = (request.POST.get('nome') or "").strip()

        if not nome:
            return JsonResponse({
                'success': False,
                'error': 'Nome obrigatório'
            })

        categoria = editar_categoria(id, request.user, nome)

        return JsonResponse({
            'success': True,
            'nome': categoria.nome
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


#  EXCLUIR
@login_required
def excluir_categoria_view(request, id):

    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Método inválido'
        }, status=405)

    try:
        excluir_categoria(id, request.user)

        return JsonResponse({
            'success': True
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)