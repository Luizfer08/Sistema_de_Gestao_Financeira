from financeiro.models import Receita
from django.db.models import Sum


def criar(usuario, data):
    return Receita.objects.create(
        usuario=usuario,
        descricao=data.get('descricao'),
        valor=data.get('valor'),
        data=data.get('data'),
        categoria_id=int(data.get('categoria')),
        recorrente=bool(data.get('recorrente'))
    )

def listar_por_usuario(usuario):
    return Receita.objects.filter(usuario=usuario).order_by('-data')

def obter_por_id(id, usuario):
    return Receita.objects.filter(id=id, usuario=usuario).first()

def atualizar(receita, data):
    receita.descricao = data.get('descricao')
    receita.valor = data.get('valor')
    receita.data = data.get('data')
    receita.categoria_id = int(data.get('categoria'))
    receita.recorrente = bool(data.get('recorrente'))

    receita.save()
    return receita

def deletar(receita):
    receita.delete()

def somar_receitas(usuario):
    return Receita.objects.filter(
        usuario=usuario
    ).aggregate(total=Sum('valor'))['total'] or 0

def somar_receitas_por_data(usuario, data_limite):
    return Receita.objects.filter(
        usuario=usuario,
        data__lte=data_limite
    ).aggregate(total=Sum('valor'))['total'] or 0