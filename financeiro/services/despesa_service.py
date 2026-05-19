# REPOSITORY
from financeiro.repositories import despesa_repository as repo


# CRIAR DESPESA
def criar_despesa(usuario, data):

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

    # Cria despesa
    return repo.criar(
        usuario,
        data
    )


# TOTAL GERAL DE DESPESAS
def total_despesas(usuario):

    return repo.somar_despesas(
        usuario
    )


# TOTAL DE DESPESAS ATÉ DATA
def total_despesas_por_data(usuario, data):

    return repo.somar_despesas_por_data(
        usuario,
        data
    )


# TOTAL DE DESPESAS POR PERÍODO
def total_despesas_por_periodo(usuario, data_inicio, data_fim):

    return repo.somar_despesas_por_periodo(
        usuario,
        data_inicio,
        data_fim
    )


# LISTAR TODAS AS DESPESAS
def listar_despesas(usuario):

    return repo.listar_por_usuario(
        usuario
    )


# LISTAR DESPESAS POR PERÍODO
def listar_despesas_por_periodo(usuario, data_inicio, data_fim):

    return repo.listar_por_periodo(
        usuario,
        data_inicio,
        data_fim
    )


# EDITAR DESPESA
def editar_despesa(id, usuario, data):

    # Busca despesa
    despesa = repo.obter_por_id(
        id,
        usuario
    )

    # Verifica se despesa existe
    if not despesa:

        raise ValueError(
            "Despesa não encontrada"
        )

    # Atualiza despesa
    return repo.atualizar(
        despesa,
        data
    )


# EXCLUIR DESPESA
def excluir_despesa(id, usuario):

    # Busca despesa
    despesa = repo.obter_por_id(
        id,
        usuario
    )

    # Verifica se despesa existe
    if not despesa:

        raise ValueError(
            "Despesa não encontrada"
        )

    # Remove despesa
    repo.deletar(despesa)