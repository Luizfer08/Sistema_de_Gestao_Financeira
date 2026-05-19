# REPOSITORY
from financeiro.repositories import categoria_repository as repo

# MODELS
from financeiro.models import Categoria


# CORES PERMITIDAS NO SISTEMA
CORES_PERMITIDAS = {
    '#8FEBDD', '#62BFF0', '#5A4226', '#FFA0A4', '#399886',
    '#858585', '#C7C7CD', '#08AF4A', '#594CF2', '#A30CE9',
    '#FEAB1B', '#E26CE1', '#99F69D', '#8D8D8D', '#FF073F',
    '#B775C5', '#918F5E', '#FFA5B5', '#FF7B00', '#1E29ED',
    '#18BEEA', '#F5D7B8',
}


# VALIDA TIPO DA CATEGORIA
def normalizar_tipo(tipo):

    # Verifica se o tipo informado é válido
    if tipo not in {
        Categoria.TIPO_RECEITA,
        Categoria.TIPO_DESPESA
    }:

        raise ValueError(
            "Tipo de categoria invalido"
        )

    return tipo


# VALIDA COR DA CATEGORIA
def normalizar_cor(cor):

    # Define cor padrão caso não exista
    cor = (cor or '#8FEBDD').upper()

    # Verifica se a cor é permitida
    if cor not in CORES_PERMITIDAS:

        raise ValueError(
            "Cor de categoria invalida"
        )

    return cor


# CRIAR CATEGORIA
def criar_categoria(usuario, nome, tipo, cor):

    # Valida nome obrigatório
    if not nome:

        raise ValueError(
            "Nome da categoria e obrigatorio"
        )

    # Cria categoria
    return repo.criar(
        usuario,
        nome,
        normalizar_tipo(tipo),
        normalizar_cor(cor)
    )


# LISTAR CATEGORIAS
def listar_categorias(usuario, tipo=None):

    # Valida tipo caso informado
    if tipo:

        tipo = normalizar_tipo(tipo)

    # Retorna categorias do usuário
    return repo.listar_por_usuario(
        usuario,
        tipo
    )


# EDITAR CATEGORIA
def editar_categoria(id, usuario, nome, cor=None):

    # Busca categoria
    categoria = repo.obter_por_id(
        id,
        usuario
    )

    # Verifica se categoria existe
    if not categoria:

        raise ValueError(
            "Categoria nao encontrada"
        )

    # Valida nome obrigatório
    if not nome:

        raise ValueError(
            "Nome nao pode ser vazio"
        )

    # Atualiza categoria
    return repo.atualizar(
        categoria,
        nome,
        normalizar_cor(cor) if cor else None
    )


# EXCLUIR CATEGORIA
def excluir_categoria(id, usuario):

    # Busca categoria
    categoria = repo.obter_por_id(
        id,
        usuario
    )

    # Verifica se categoria existe
    if not categoria:

        raise ValueError(
            "Categoria nao encontrada"
        )

    # Remove categoria
    repo.deletar(categoria)