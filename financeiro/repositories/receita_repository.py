from financeiro.models import Receita
from financeiro.models.categoria import Categoria
from django.db.models import Sum
from datetime import datetime


def converter_data(data_str):
    """
    Converte string (YYYY-MM-DD) para objeto date
    Evita erro de strftime e inconsistência no banco
    """
    if not data_str:
        return None

    try:
        return datetime.strptime(data_str, "%Y-%m-%d").date()
    except ValueError:
        return None


# CRIAR
def criar(usuario, data):

    categoria = None
    if data.get('categoria'):
        try:
            categoria = Categoria.objects.get(id=data.get('categoria'))
        except Categoria.DoesNotExist:
            raise ValueError("Categoria inválida")

    receita = Receita.objects.create(
        usuario=usuario,
        descricao=data.get('descricao'),

        valor=float(data.get('valor')),

        data=converter_data(data.get('data')),

        categoria=categoria,

        recorrente=True if data.get('recorrente') else False,

        data_fim=converter_data(data.get('data_fim'))
    )

    return receita


# LISTAR
def listar_por_usuario(usuario):
    return Receita.objects.filter(
        usuario=usuario
    ).order_by('-data')


# OBTER
def obter_por_id(id, usuario):
    return Receita.objects.filter(
        id=id,
        usuario=usuario
    ).first()


# ATUALIZAR
def atualizar(receita, data):

    receita.descricao = data.get('descricao')

    if data.get('valor'):
        receita.valor = float(data.get('valor'))

    if data.get('data'):
        receita.data = converter_data(data.get('data'))

    if data.get('categoria'):
        try:
            receita.categoria = Categoria.objects.get(id=data.get('categoria'))
        except Categoria.DoesNotExist:
            raise ValueError("Categoria inválida")

    receita.recorrente = True if data.get('recorrente') else False

    # opcional
    receita.data_fim = converter_data(data.get('data_fim'))

    receita.save()
    return receita


# DELETAR
def deletar(receita):
    receita.delete()


# TOTAL GERAL
def somar_receitas(usuario):
    return Receita.objects.filter(
        usuario=usuario
    ).aggregate(total=Sum('valor'))['total'] or 0


# TOTAL POR DATA
def somar_receitas_por_periodo(usuario, data_inicio, data_fim):
    return Receita.objects.filter(
        usuario=usuario,
        data__range=(data_inicio, data_fim)
    ).aggregate(total=Sum('valor'))['total'] or 0

