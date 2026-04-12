# Renderização e redirecionamento
from django.shortcuts import render, redirect

# Proteção de rota
from django.contrib.auth.decorators import login_required

# Mensagens para o usuário (UX)
from django.contrib import messages

from django.http import JsonResponse

# Services (regra de negócio)
from financeiro.services.categoria_service import (
    criar_categoria,
    listar_categorias,
    editar_categoria,
    excluir_categoria
)


#  LISTAR CATEGORIAS (TELA PRINCIPAL)
@login_required
def listar_categorias_view(request):

    categorias = listar_categorias(request.user)

    return render(request, 'financeiro/categorias/listar.html', {
        'categorias': categorias
    })


#  CRIAR CATEGORIA 
@login_required
def criar_categoria_view(request):

    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')

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
            })

    return JsonResponse({'success': False})


#  EDITAR CATEGORIA
@login_required
def editar_categoria_view(request, id):

    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')

            if not nome:
                return JsonResponse({
                    'success': False,
                    'error': 'Nome obrigatório'
                })

            editar_categoria(id, request.user, nome)

            return JsonResponse({
                'success': True,
                'nome': nome
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return JsonResponse({'success': False})


# EXCLUIR CATEGORIA
@login_required
def excluir_categoria_view(request, id):

    if request.method == 'POST':
        try:
            excluir_categoria(id, request.user)

            return JsonResponse({
                'success': True
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return JsonResponse({'success': False})