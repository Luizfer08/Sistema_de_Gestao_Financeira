# Repository responsavel pelo acesso ao banco de dados de categorias.
from financeiro.models import Categoria


# Cria uma categoria para receitas ou despesas.
def criar(usuario, nome, tipo='despesa', cor='#8FEBDD'):

    return Categoria.objects.create(

        usuario=usuario,
        nome=nome,
        tipo=tipo,
        cor=cor
    )


# Lista categorias do usuario, com filtro opcional por tipo.
def listar_por_usuario(usuario, tipo=None):

    # Busca somente categorias pertencentes ao usuario logado.
    categorias = Categoria.objects.filter(
        usuario=usuario
    )

    # Quando informado, limita o resultado a receita ou despesa.
    if tipo:

        categorias = categorias.filter(
            tipo=tipo
        )

    return categorias.order_by('nome')


# Busca uma categoria pelo id garantindo que ela pertence ao usuario.
def obter_por_id(id, usuario):

    return Categoria.objects.filter(
        id=id,
        usuario=usuario
    ).first()


# Atualiza os dados editaveis da categoria.
def atualizar(categoria, nome, cor=None):

    categoria.nome = nome

    # A cor so muda quando uma nova cor e enviada.
    if cor:

        categoria.cor = cor

    categoria.save()

    return categoria


# Remove uma categoria do banco de dados.
def deletar(categoria):

    categoria.delete()
