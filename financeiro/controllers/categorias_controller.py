# RENDER / REDIRECT
from django.shortcuts import render

# SEGURANÇA
from django.contrib.auth.decorators import login_required

# JSON
from django.http import JsonResponse

# SERVICES
from financeiro.services.categoria_service import (
    criar_categoria,
    listar_categorias,
    editar_categoria,
    excluir_categoria
)


# LISTAR CATEGORIAS
@login_required
def listar_categorias_view(request):

    # Busca categorias de receita
    categorias_receita = listar_categorias(request.user, 'receita')

    # Busca categorias de despesa
    categorias_despesa = listar_categorias(request.user, 'despesa')

    # Renderiza página com dados das categorias
    return render(request, 'financeiro/categorias/listar.html', {
        'categorias_receita': categorias_receita,
        'categorias_despesa': categorias_despesa,

        # Soma total de categorias cadastradas
        'total_categorias': categorias_receita.count() + categorias_despesa.count()
    })


# CRIAR CATEGORIA
@login_required
def criar_categoria_view(request):

    # Valida método da requisição
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Método inválido'
        }, status=405)

    try:

        # Obtém dados enviados pelo formulário
        nome = (request.POST.get('nome') or "").strip()
        tipo = (request.POST.get('tipo') or "").strip()
        cor = (request.POST.get('cor') or "").strip()

        # Valida nome obrigatório
        if not nome:
            return JsonResponse({
                'success': False,
                'error': 'Nome obrigatório'
            })

        # Cria categoria
        categoria = criar_categoria(request.user, nome, tipo, cor)

        # Retorna dados da categoria criada
        return JsonResponse({
            'success': True,
            'id': categoria.id,
            'nome': categoria.nome,
            'tipo': categoria.tipo,
            'cor': categoria.cor
        })

    # Captura erros da operação
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


# EDITAR CATEGORIA
@login_required
def editar_categoria_view(request, id):

    # Valida método da requisição
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Método inválido'
        }, status=405)

    try:

        # Obtém dados enviados pelo formulário
        nome = (request.POST.get('nome') or "").strip()
        cor = (request.POST.get('cor') or "").strip()

        # Valida nome obrigatório
        if not nome:
            return JsonResponse({
                'success': False,
                'error': 'Nome obrigatório'
            })

        # Atualiza categoria
        categoria = editar_categoria(id, request.user, nome, cor)

        # Retorna dados atualizados
        return JsonResponse({
            'success': True,
            'nome': categoria.nome,
            'cor': categoria.cor
        })

    # Captura erros da operação
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


# EXCLUIR CATEGORIA
@login_required
def excluir_categoria_view(request, id):

    # Valida método da requisição
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Método inválido'
        }, status=405)

    try:

        # Remove categoria
        excluir_categoria(id, request.user)

        # Retorna sucesso da operação
        return JsonResponse({
            'success': True
        })

    # Captura erros da operação
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)