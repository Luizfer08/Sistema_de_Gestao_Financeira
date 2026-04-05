from financeiro.repositories import despesa_repository as repo
from financeiro.models.despesa import Despesa
from django.db.models import Sum


def criar_despesa(usuario, data):
    """
    Valida e cria uma nova despesa.
    Aplica regras de negócio antes de salvar.
    """
    valor = data.get('valor')

    if not valor:
        raise ValueError("O campo valor é obrigatório")

    try:
        valor = float(valor)
    except:
        raise ValueError("Valor inválido")

    if valor <= 0:
        raise ValueError("Valor deve ser maior que zero")

    if not data.get('data'):
        raise ValueError("A data é obrigatória")

    if not data.get('categoria'):
        raise ValueError("Selecione uma categoria")

    return repo.criar(usuario, data)

def total_despesas(usuario):
    """
    Retorna o total de despesas do usuário.
    """
    return repo.somar_despesas(usuario)



def total_despesas_por_data(user, data):
    """
    Retorna o total de despesas até uma data específica.
    Usado no cálculo do saldo futuro.
    """

    resultado = Despesa.objects.filter(
        usuario=user,
        data__lte=data  
    ).aggregate(total=Sum('valor'))

    return resultado['total'] or 0

def listar_despesas(usuario):
    """
    Lista todas as despesas do usuário.
    """
    return repo.listar_por_usuario(usuario)

def editar_despesa(id, usuario, data):
    """
    Atualiza uma despesa existente com validações.
    """

    despesa = repo.obter_por_id(id, usuario)

    if not despesa:
        raise ValueError("Despesa não encontrada")

    valor = data.get('valor')

    if valor:
        try:
            valor = float(valor)
        except:
            raise ValueError("Valor inválido")

        if valor <= 0:
            raise ValueError("Valor deve ser maior que zero")

    return repo.atualizar(despesa, data)

def excluir_despesa(id, usuario):
    """
    Remove uma despesa do sistema.
    """

    despesa = repo.obter_por_id(id, usuario)

    if not despesa:
        raise ValueError("Despesa não encontrada")

    repo.deletar(despesa)

def total_despesas_por_periodo(user, data_inicio, data_fim):
    """
    Retorna despesas dentro de um período.
    Ideal para gráficos mensais e relatórios.
    """

    resultado = Despesa.objects.filter(
        usuario=user,
        data__range=(data_inicio, data_fim)
    ).aggregate(total=Sum('valor'))

    return resultado['total'] or 0