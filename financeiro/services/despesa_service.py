# Service responsavel pelas regras de negocio de despesas.
from financeiro.repositories import despesa_repository as repo


# Valida e cria uma despesa.
def criar_despesa(usuario, data):

    # Valor e obrigatorio porque participa dos calculos financeiros.
    valor = data.get('valor')

    if not valor:

        raise ValueError(
            "Valor e obrigatorio"
        )

    try:

        # Converte para numero antes de validar se e positivo.
        valor = float(valor)

    except:

        raise ValueError(
            "Valor invalido"
        )

    # Despesas com valor zero ou negativo nao devem ser cadastradas.
    if valor <= 0:

        raise ValueError(
            "Valor deve ser maior que zero"
        )

    return repo.criar(
        usuario,
        data
    )


# Retorna o total geral de despesas do usuario.
def total_despesas(usuario):

    return repo.somar_despesas(
        usuario
    )


# Retorna o total de despesas ate uma data.
def total_despesas_por_data(usuario, data):

    return repo.somar_despesas_por_data(
        usuario,
        data
    )


# Retorna o total de despesas dentro de uma competencia.
def total_despesas_por_periodo(usuario, data_inicio, data_fim):

    return repo.somar_despesas_por_periodo(
        usuario,
        data_inicio,
        data_fim
    )


# Lista todas as despesas cadastradas pelo usuario.
def listar_despesas(usuario):

    return repo.listar_por_usuario(
        usuario
    )


# Lista despesas validas para o periodo selecionado.
def listar_despesas_por_periodo(usuario, data_inicio, data_fim):

    return repo.listar_por_periodo(
        usuario,
        data_inicio,
        data_fim
    )


# Edita uma despesa existente.
def editar_despesa(id, usuario, data):

    # Garante que o usuario so edite despesas proprias.
    despesa = repo.obter_por_id(
        id,
        usuario
    )

    if not despesa:

        raise ValueError(
            "Despesa nao encontrada"
        )

    return repo.atualizar(
        despesa,
        data
    )


# Exclui uma despesa existente.
def excluir_despesa(id, usuario):

    # Garante que o usuario so exclua despesas proprias.
    despesa = repo.obter_por_id(
        id,
        usuario
    )

    if not despesa:

        raise ValueError(
            "Despesa nao encontrada"
        )

    repo.deletar(despesa)
