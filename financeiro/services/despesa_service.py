from financeiro.repositories import despesa_repository as repo


#  CRIAR 
def criar_despesa(usuario, data):

    valor = data.get('valor')

    if not valor:
        raise ValueError("Valor é obrigatório")

    try:
        valor = float(valor)
    except:
        raise ValueError("Valor inválido")

    if valor <= 0:
        raise ValueError("Valor deve ser maior que zero")

    return repo.criar(usuario, data)


#  TOTAL GERAL 
def total_despesas(usuario):
    return repo.somar_despesas(usuario)


#  ATÉ DATA 
def total_despesas_por_data(usuario, data):
    return repo.somar_despesas_por_data(usuario, data)


#  PERÍODO
def total_despesas_por_periodo(usuario, data_inicio, data_fim):
    return repo.somar_despesas_por_periodo(
        usuario,
        data_inicio,
        data_fim
    )


#  LISTAR 
def listar_despesas(usuario):
    return repo.listar_por_usuario(usuario)


#  EDITAR 
def editar_despesa(id, usuario, data):

    despesa = repo.obter_por_id(id, usuario)

    if not despesa:
        raise ValueError("Despesa não encontrada")

    return repo.atualizar(despesa, data)


#  EXCLUIR 
def excluir_despesa(id, usuario):

    despesa = repo.obter_por_id(id, usuario)

    if not despesa:
        raise ValueError("Despesa não encontrada")

    repo.deletar(despesa)