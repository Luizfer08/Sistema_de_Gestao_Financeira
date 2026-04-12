from financeiro.models.despesa import Despesa
from financeiro.models.categoria import Categoria
from django.db.models import Sum
from datetime import datetime


def converter_data(data_str):
    """
    Converte string (YYYY-MM-DD) para date
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

    despesa = Despesa.objects.create(
        usuario=usuario,
        descricao=data.get('descricao'),

        valor=float(data.get('valor')),

        data=converter_data(data.get('data')),

        categoria=categoria,

        recorrente=True if data.get('recorrente') else False,

        data_fim=converter_data(data.get('data_fim'))
    )

    return despesa


# LISTAR
def listar_por_usuario(usuario):
    return Despesa.objects.filter(
        usuario=usuario
    ).order_by('-data')


# OBTER
def obter_por_id(id, usuario):
    return Despesa.objects.filter(
        id=id,
        usuario=usuario
    ).first()


# ATUALIZAR
def atualizar(despesa, data):

    despesa.descricao = data.get('descricao')

    if data.get('valor'):
        despesa.valor = float(data.get('valor'))

    if data.get('data'):
        despesa.data = converter_data(data.get('data'))

    if data.get('categoria'):
        try:
            despesa.categoria = Categoria.objects.get(id=data.get('categoria'))
        except Categoria.DoesNotExist:
            raise ValueError("Categoria inválida")

    despesa.recorrente = True if data.get('recorrente') else False

    despesa.data_fim = converter_data(data.get('data_fim'))

    despesa.save()
    return despesa


# DELETAR
def deletar(despesa):
    despesa.delete()


# TOTAL GERAL
def somar_despesas(usuario):
    return Despesa.objects.filter(
        usuario=usuario
    ).aggregate(total=Sum('valor'))['total'] or 0


# TOTAL POR DATA
def somar_despesas_por_periodo(usuario, data_inicio, data_fim):
    return Despesa.objects.filter(
        usuario=usuario,
        data__range=(data_inicio, data_fim)
    ).aggregate(total=Sum('valor'))['total'] or 0