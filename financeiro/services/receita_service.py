# REPOSITORY
from financeiro.repositories import receita_repository as repo


# CRIAR RECEITA
def criar_receita(usuario, data):

    # Obtém valor informado
    valor = data.get('valor')

    # Valida valor obrigatório
    if not valor:

        raise ValueError(
            "Valor é obrigatório"
        )

    try:

        # Converte valor para float
        valor = float(valor)

    # Valor inválido
    except:

        raise ValueError(
            "Valor inválido"
        )

    # Valida valor positivo
    if valor <= 0:

        raise ValueError(
            "Valor deve ser maior que zero"
        )

    # Cria receita
    return repo.criar(
        usuario,
        data
    )


# TOTAL GERAL DE RECEITAS
def total_receitas(usuario):

    return repo.somar_receitas(
        usuario
    )


# TOTAL DE RECEITAS ATÉ DATA
def total_receitas_por_data(usuario, data):

    return repo.somar_receitas_por_data(
        usuario,
        data
    )


# TOTAL DE RECEITAS POR PERÍODO
def total_receitas_por_periodo(usuario, data_inicio, data_fim):

    return repo.somar_receitas_por_periodo(
        usuario,
        data_inicio,
        data_fim
    )


# LISTAR TODAS AS RECEITAS
def listar_receitas(usuario):

    return repo.listar_por_usuario(
        usuario
    )


# LISTAR RECEITAS POR PERÍODO
def listar_receitas_por_periodo(usuario, data_inicio, data_fim):

    return repo.listar_por_periodo(
        usuario,
        data_inicio,
        data_fim
    )


# EDITAR RECEITA
def editar_receita(id, usuario, data):

    # Busca receita
    receita = repo.obter_por_id(
        id,
        usuario
    )

    # Verifica se receita existe
    if not receita:

        raise ValueError(
            "Receita não encontrada"
        )

    # Atualiza receita
    return repo.atualizar(
        receita,
        data
    )


# EXCLUIR RECEITA
def excluir_receita(id, usuario):

    # Busca receita
    receita = repo.obter_por_id(
        id,
        usuario
    )

    # Verifica se receita existe
    if not receita:

        raise ValueError(
            "Receita não encontrada"
        )

    # Remove receita
    repo.deletar(receita)