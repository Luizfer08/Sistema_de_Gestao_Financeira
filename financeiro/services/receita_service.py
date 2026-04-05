from financeiro.repositories import receita_repository as repo
from financeiro.models.receita import Receita
from django.db.models import Sum



def criar_receita(usuario, data):
    """
    Responsável por validar e criar uma nova receita.
    Aplica regras de negócio antes de persistir no banco.
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

    return repo.criar(usuario, data)

def total_receitas(usuario):
    """
    Retorna o total de receitas do usuário.
    """
    return repo.somar_receitas(usuario)

def total_receitas_por_data(user, data):
    """
    Retorna o total de receitas até uma data específica.
    Utilizado no cálculo de saldo futuro.
    """

    resultado = Receita.objects.filter(
        usuario=user,
        data__lte=data  
    ).aggregate(total=Sum('valor'))

    return resultado['total'] or 0


def listar_receitas(usuario):
    """
    Retorna todas as receitas do usuário.
    """
    return repo.listar_por_usuario(usuario)

def editar_receita(id, usuario, data):
    """
    Atualiza uma receita existente com validações.
    """

    receita = repo.obter_por_id(id, usuario)

    if not receita:
        raise ValueError("Receita não encontrada")

    valor = data.get('valor')

    if valor:
        try:
            valor = float(valor)
        except:
            raise ValueError("Valor inválido")

        if valor <= 0:
            raise ValueError("Valor deve ser maior que zero")

    return repo.atualizar(receita, data)

def excluir_receita(id, usuario):
    """
    Remove uma receita do sistema.
    """

    receita = repo.obter_por_id(id, usuario)

    if not receita:
        raise ValueError("Receita não encontrada")

    repo.deletar(receita)

def total_receitas_por_periodo(user, data_inicio, data_fim):
    """
    Retorna receitas dentro de um período.
    Pode ser usado futuramente para gráficos mensais.
    """

    resultado = Receita.objects.filter(
        usuario=user,
        data__range=(data_inicio, data_fim)
    ).aggregate(total=Sum('valor'))

    return resultado['total'] or 0