from django.db.models import Sum
from financeiro.models import Receita, Despesa

def calcular_resumo(usuario, data=None):
    receitas = Receita.objects.filter(usuario=usuario)
    despesas = Despesa.objects.filter(usuario=usuario)

    if data:
        receitas = receitas.filter(data__lte=data)
        despesas = despesas.filter(data__lte=data)

    total_receitas = receitas.aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = despesas.aggregate(Sum('valor'))['valor__sum'] or 0

    saldo = total_receitas - total_despesas

    return total_receitas, total_despesas, saldo