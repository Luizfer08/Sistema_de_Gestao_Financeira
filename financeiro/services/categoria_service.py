# Service responsavel pelas regras de negocio de categorias.
from financeiro.repositories import categoria_repository as repo

# Categoria fornece os tipos validos: receita e despesa.
from financeiro.models import Categoria


# Paleta permitida para manter consistencia visual entre telas e graficos.
CORES_PERMITIDAS = {
    '#8FEBDD', '#62BFF0', '#5A4226', '#FFA0A4', '#399886',
    '#858585', '#C7C7CD', '#08AF4A', '#594CF2', '#A30CE9',
    '#FEAB1B', '#E26CE1', '#99F69D', '#8D8D8D', '#FF073F',
    '#B775C5', '#918F5E', '#FFA5B5', '#FF7B00', '#1E29ED',
    '#18BEEA', '#F5D7B8',
}


# Garante que a categoria seja de receita ou despesa.
def normalizar_tipo(tipo):

    if tipo not in {
        Categoria.TIPO_RECEITA,
        Categoria.TIPO_DESPESA
    }:

        raise ValueError(
            "Tipo de categoria invalido"
        )

    return tipo


# Garante que a cor enviada esteja dentro da paleta cadastrada.
def normalizar_cor(cor):

    cor = (cor or '#8FEBDD').upper()

    if cor not in CORES_PERMITIDAS:

        raise ValueError(
            "Cor de categoria invalida"
        )

    return cor


# Cria uma categoria apos validar nome, tipo e cor.
def criar_categoria(usuario, nome, tipo, cor):

    if not nome:

        raise ValueError(
            "Nome da categoria e obrigatorio"
        )

    return repo.criar(
        usuario,
        nome,
        normalizar_tipo(tipo),
        normalizar_cor(cor)
    )


# Lista categorias do usuario, com filtro opcional por tipo.
def listar_categorias(usuario, tipo=None):

    if tipo:

        tipo = normalizar_tipo(tipo)

    return repo.listar_por_usuario(
        usuario,
        tipo
    )


# Edita uma categoria existente.
def editar_categoria(id, usuario, nome, cor=None):

    # Garante que o usuario so edite categorias proprias.
    categoria = repo.obter_por_id(
        id,
        usuario
    )

    if not categoria:

        raise ValueError(
            "Categoria nao encontrada"
        )

    if not nome:

        raise ValueError(
            "Nome nao pode ser vazio"
        )

    return repo.atualizar(
        categoria,
        nome,
        normalizar_cor(cor) if cor else None
    )


# Exclui uma categoria e remove os lancamentos vinculados a ela.
def excluir_categoria(id, usuario):

    # Garante que o usuario so exclua categorias proprias.
    categoria = repo.obter_por_id(
        id,
        usuario
    )

    if not categoria:

        raise ValueError(
            "Categoria nao encontrada"
        )

    # Receitas e despesas vinculadas sao removidas antes da categoria.
    categoria.receitas.all().delete()
    categoria.despesas.all().delete()

    repo.deletar(categoria)
