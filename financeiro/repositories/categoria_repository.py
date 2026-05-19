# MODELS
from financeiro.models import Categoria


# CRIA NOVA CATEGORIA
def criar(usuario, nome, tipo='despesa', cor='#8FEBDD'):

    return Categoria.objects.create(

        # Usuário dono da categoria
        usuario=usuario,

        # Nome da categoria
        nome=nome,

        # Tipo da categoria
        tipo=tipo,

        # Cor utilizada na interface
        cor=cor
    )


# LISTA CATEGORIAS DO USUÁRIO
def listar_por_usuario(usuario, tipo=None):

    # Busca categorias do usuário
    categorias = Categoria.objects.filter(
        usuario=usuario
    )

    # Filtra por tipo caso informado
    if tipo:

        categorias = categorias.filter(
            tipo=tipo
        )

    # Ordena categorias por nome
    return categorias.order_by('nome')


# BUSCA CATEGORIA PELO ID
def obter_por_id(id, usuario):

    return Categoria.objects.filter(
        id=id,
        usuario=usuario
    ).first()


# ATUALIZA CATEGORIA
def atualizar(categoria, nome, cor=None):

    # Atualiza nome
    categoria.nome = nome

    # Atualiza cor caso informada
    if cor:

        categoria.cor = cor

    # Salva alterações
    categoria.save()

    return categoria


# REMOVE CATEGORIA
def deletar(categoria):

    categoria.delete()