# Service responsavel pelas regras de negocio de receitas.
from financeiro.repositories import receita_repository as repo


# Valida e cria uma receita.
def criar_receita(usuario, data):

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

    # Receitas com valor zero ou negativo nao devem ser cadastradas.
    if valor <= 0:

        raise ValueError(
            "Valor deve ser maior que zero"
        )

    return repo.criar(
        usuario,
        data
    )


# Retorna o total geral de receitas do usuario.
def total_receitas(usuario):

    return repo.somar_receitas(
        usuario
    )


# Retorna o total de receitas ate uma data.
def total_receitas_por_data(usuario, data):

    return repo.somar_receitas_por_data(
        usuario,
        data
    )


# Retorna o total de receitas dentro de uma competencia.
def total_receitas_por_periodo(usuario, data_inicio, data_fim):

    return repo.somar_receitas_por_periodo(
        usuario,
        data_inicio,
        data_fim
    )


# Lista todas as receitas cadastradas pelo usuario.
def listar_receitas(usuario):

    return repo.listar_por_usuario(
        usuario
    )


# Lista receitas validas para o periodo selecionado.
def listar_receitas_por_periodo(usuario, data_inicio, data_fim):

    return repo.listar_por_periodo(
        usuario,
        data_inicio,
        data_fim
    )


# Edita uma receita existente.
def editar_receita(id, usuario, data):

    # Garante que o usuario so edite receitas proprias.
    receita = repo.obter_por_id(
        id,
        usuario
    )

    if not receita:

        raise ValueError(
            "Receita nao encontrada"
        )

    return repo.atualizar(
        receita,
        data
    )


# Exclui uma receita existente.
def excluir_receita(id, usuario):

    # Garante que o usuario so exclua receitas proprias.
    receita = repo.obter_por_id(
        id,
        usuario
    )

    if not receita:

        raise ValueError(
            "Receita nao encontrada"
        )

    repo.deletar(receita)
