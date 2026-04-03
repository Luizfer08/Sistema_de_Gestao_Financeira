from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from financeiro.services.despesa_service import (
    criar_despesa,
    listar_despesas,
    editar_despesa,
    excluir_despesa
)

from financeiro.models import Categoria


@login_required
def listar_despesas_view(request):

    despesas = listar_despesas(request.user)

    return render(request, 'financeiro/despesas/listar.html', {
        'despesas': despesas
    })

@login_required
def criar_despesa_view(request):

    if request.method == 'POST':
        try:
            criar_despesa(request.user, request.POST)
            return redirect('financeiro:listar_despesas')

        except Exception as e:
            print("ERRO:", e)
            messages.error(request, str(e))

    categorias = Categoria.objects.filter(usuario=request.user)

    return render(request, 'financeiro/despesas/criar.html', {
        'categorias': categorias
    })


@login_required
def editar_despesa_view(request, id):

    categorias = Categoria.objects.filter(usuario=request.user)

    if request.method == 'POST':
        try:
            editar_despesa(id, request.user, request.POST)
            return redirect('financeiro:listar_despesas')

        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'financeiro/despesas/editar.html', {
        'categorias': categorias
    })


@login_required
def excluir_despesa_view(request, id):

    try:
        excluir_despesa(id, request.user)
    except Exception as e:
        messages.error(request, str(e))

    return redirect('financeiro:listar_despesas')