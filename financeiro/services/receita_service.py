from financeiro.repositories import receita_repository as repo


def criar_receita(usuario, data):

    # regra de negócio
    if float(data.get('valor', 0)) <= 0:
        raise ValueError("Valor deve ser maior que zero")

    return repo.criar(usuario, data)

def total_receitas(usuario):
    return repo.somar_receitas(usuario)

def total_receitas_por_data(usuario, data):
    return repo.somar_receitas_por_data(usuario, data)


def listar_receitas(usuario):
    return repo.listar_por_usuario(usuario)


def editar_receita(id, usuario, data):

    receita = repo.obter_por_id(id, usuario)

    if not receita:
        raise ValueError("Receita não encontrada")

    if float(data.get('valor', 0)) <= 0:
        raise ValueError("Valor inválido")

    return repo.atualizar(receita, data)


def excluir_receita(id, usuario):

    receita = repo.obter_por_id(id, usuario)

    if not receita:
        raise ValueError("Receita não encontrada")

    repo.deletar(receita)