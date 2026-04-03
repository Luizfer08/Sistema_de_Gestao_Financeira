from financeiro.repositories import despesa_repository as repo


from financeiro.repositories import despesa_repository as repo


def criar_despesa(usuario, data):

    valor = data.get('valor')
    if not valor:
        raise ValueError("O campo valor é obrigatório")

    try:
        valor = float(valor)
    except:
        raise ValueError("Valor inválido")

    if valor <= 0:
        raise ValueError("Valor deve ser maior que zero")

    categoria = data.get('categoria')
    if not categoria:
        raise ValueError("Selecione uma categoria")

    data_lancamento = data.get('data')
    if not data_lancamento:
        raise ValueError("A data é obrigatória")

    return repo.criar(usuario, data)

def total_despesas(usuario):
    return repo.somar_despesas(usuario)

def total_despesas_por_data(usuario, data):
    return repo.somar_despesas_por_data(usuario, data)

def listar_despesas(usuario):
    return repo.listar_por_usuario(usuario)


def editar_despesa(id, usuario, data):

    despesa = repo.obter_por_id(id, usuario)

    if not despesa:
        raise ValueError("Despesa não encontrada")

    return repo.atualizar(despesa, data)


def excluir_despesa(id, usuario):

    despesa = repo.obter_por_id(id, usuario)

    if not despesa:
        raise ValueError("Despesa não encontrada")

    repo.deletar(despesa)