from financeiro.repositories import categoria_repository as repo


def criar_categoria(usuario, nome):

    if not nome:
        raise ValueError("Nome da categoria é obrigatório")

    return repo.criar(usuario, nome)


def listar_categorias(usuario):
    return repo.listar_por_usuario(usuario)


def editar_categoria(id, usuario, nome):

    categoria = repo.obter_por_id(id, usuario)

    if not categoria:
        raise ValueError("Categoria não encontrada")

    if not nome:
        raise ValueError("Nome não pode ser vazio")

    return repo.atualizar(categoria, nome)


def excluir_categoria(id, usuario):

    categoria = repo.obter_por_id(id, usuario)

    if not categoria:
        raise ValueError("Categoria não encontrada")

    repo.deletar(categoria)