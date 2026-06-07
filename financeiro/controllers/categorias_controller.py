# Render devolve a pagina HTML de categorias.
from django.shortcuts import render

# Login_required protege a tela para usuarios autenticados.
from django.contrib.auth.decorators import login_required

# JsonResponse devolve respostas para chamadas AJAX.
from django.http import JsonResponse

# Services concentram as regras de negocio de categorias.
from financeiro.services.categoria_service import (
    criar_categoria,
    listar_categorias,
    editar_categoria,
    excluir_categoria
)


# Renderiza a tela de categorias separando receitas e despesas.
@login_required
def listar_categorias_view(request):

    # Categorias de receita aparecem apenas em telas de receita.
    categorias_receita = listar_categorias(request.user, 'receita')

    # Categorias de despesa aparecem apenas em telas de despesa.
    categorias_despesa = listar_categorias(request.user, 'despesa')

    return render(request, 'financeiro/categorias/listar.html', {
        'categorias_receita': categorias_receita,
        'categorias_despesa': categorias_despesa,

        # Total usado no contador da tela.
        'total_categorias': categorias_receita.count() + categorias_despesa.count()
    })


# Cria uma categoria por requisicao AJAX.
@login_required
def criar_categoria_view(request):

    # Criacao deve acontecer apenas por POST.
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Metodo invalido'
        }, status=405)

    try:

        # Dados recebidos do popup de categoria.
        nome = (request.POST.get('nome') or "").strip()
        tipo = (request.POST.get('tipo') or "").strip()
        cor = (request.POST.get('cor') or "").strip()

        if not nome:
            return JsonResponse({
                'success': False,
                'error': 'Nome obrigatorio'
            })

        categoria = criar_categoria(request.user, nome, tipo, cor)

        # Retorna os dados para o JavaScript atualizar a tabela.
        return JsonResponse({
            'success': True,
            'id': categoria.id,
            'nome': categoria.nome,
            'tipo': categoria.tipo,
            'cor': categoria.cor
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


# Edita uma categoria por requisicao AJAX.
@login_required
def editar_categoria_view(request, id):

    # Edicao deve acontecer apenas por POST.
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Metodo invalido'
        }, status=405)

    try:

        # Nome e cor sao os campos editaveis.
        nome = (request.POST.get('nome') or "").strip()
        cor = (request.POST.get('cor') or "").strip()

        if not nome:
            return JsonResponse({
                'success': False,
                'error': 'Nome obrigatorio'
            })

        categoria = editar_categoria(id, request.user, nome, cor)

        # Retorna os dados atualizados para o JavaScript.
        return JsonResponse({
            'success': True,
            'nome': categoria.nome,
            'cor': categoria.cor
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


# Exclui uma categoria por requisicao AJAX.
@login_required
def excluir_categoria_view(request, id):

    # Exclusao deve acontecer apenas por POST.
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Metodo invalido'
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
