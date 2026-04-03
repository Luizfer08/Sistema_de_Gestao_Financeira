from financeiro.models import Despesa
from django.db.models import Sum


def criar(usuario, data):

    data_fim = data.get('data_fim')

    if not data_fim:
        data_fim = None

    return Despesa.objects.create(
        usuario=usuario,
        descricao=data.get('descricao'),
        valor=data.get('valor'),
        data=data.get('data'),
        data_fim=data_fim,
        categoria_id=int(data.get('categoria')),
        recorrente=bool(data.get('recorrente'))
    )

def listar_por_usuario(usuario):
    return Despesa.objects.filter(usuario=usuario).order_by('-data')

def obter_por_id(id, usuario):
    return Despesa.objects.filter(id=id, usuario=usuario).first()

def atualizar(despesa, data):

    data_fim = data.get('data_fim')

    if not data_fim:
        data_fim = None

    despesa.descricao = data.get('descricao')
    despesa.valor = data.get('valor')
    despesa.data = data.get('data')
    despesa.data_fim = data_fim
    despesa.categoria_id = int(data.get('categoria'))
    despesa.recorrente = bool(data.get('recorrente'))

    despesa.save()
    return despesa

def deletar(despesa):
    despesa.delete()

def somar_despesas(usuario):
    return Despesa.objects.filter(
        usuario=usuario
    ).aggregate(total=Sum('valor'))['total'] or 0

def somar_despesas_por_data(usuario, data_limite):
    return Despesa.objects.filter(
        usuario=usuario,
        data__lte=data_limite
    ).aggregate(total=Sum('valor'))['total'] or 0