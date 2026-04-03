from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from financeiro.services.categoria_service import (
    criar_categoria,
    listar_categorias,
    editar_categoria,
    excluir_categoria
)


@login_required
def listar_categorias_view(request):

    categorias = listar_categorias(request.user)

    return render(request, 'financeiro/categorias/listar.html', {
        'categorias': categorias
    })

@login_required
def criar_categoria_view(request):

    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            criar_categoria(request.user, nome)

            return redirect('financeiro:listar_categorias')

        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'financeiro/categorias/criar.html')

@login_required
def editar_categoria_view(request, id):

    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            editar_categoria(id, request.user, nome)

            return redirect('financeiro:listar_categorias')

        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'financeiro/categorias/editar.html')

@login_required
def excluir_categoria_view(request, id):

    try:
        excluir_categoria(id, request.user)

    except Exception as e:
        messages.error(request, str(e))

    return redirect('financeiro:listar_categorias')