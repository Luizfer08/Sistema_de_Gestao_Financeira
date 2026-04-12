from financeiro.repositories import receita_repository as repo


#  CRIAR 
def criar_receita(usuario, data):

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
def total_receitas(usuario):
    return repo.somar_receitas(usuario)


#  ATÉ DATA  
def total_receitas_por_data(usuario, data):
    return repo.somar_receitas_por_data(usuario, data)


#  PERÍODO  
def total_receitas_por_periodo(usuario, data_inicio, data_fim):
    return repo.somar_receitas_por_periodo(
        usuario,
        data_inicio,
        data_fim
    )


#  LISTAR 
def listar_receitas(usuario):
    return repo.listar_por_usuario(usuario)


#  EDITAR 
def editar_receita(id, usuario, data):

    receita = repo.obter_por_id(id, usuario)

    if not receita:
        raise ValueError("Receita não encontrada")

    return repo.atualizar(receita, data)


#  EXCLUIR 
def excluir_receita(id, usuario):

    receita = repo.obter_por_id(id, usuario)

    if not receita:
        raise ValueError("Receita não encontrada")

    repo.deletar(receita)