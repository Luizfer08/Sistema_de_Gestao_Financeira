from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

    return render(request, 'financeiro/receitas/listar.html', {
        'receitas': receitas
    })

@login_required
def criar_receita_view(request):

    if request.method == 'POST':
        try:
            criar_receita(request.user, request.POST)
            return redirect('financeiro:listar_receitas')

        except Exception as e:
            messages.error(request, str(e))

    categorias = Categoria.objects.filter(usuario=request.user)

    return render(request, 'financeiro/receitas/criar.html', {
        'categorias': categorias
    })

@login_required
def editar_receita_view(request, id):

    categorias = Categoria.objects.filter(usuario=request.user)

    if request.method == 'POST':
        try:
            editar_receita(id, request.user, request.POST)
            return redirect('financeiro:listar_receitas')

        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'financeiro/receitas/editar.html', {
        'categorias': categorias
    })


@login_required
def excluir_receita_view(request, id):

    try:
        excluir_receita(id, request.user)

    except Exception as e:
        messages.error(request, str(e))

    return redirect('financeiro:listar_receitas')