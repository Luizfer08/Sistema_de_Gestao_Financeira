from financeiro.models import Categoria


def criar(usuario, nome):
    return Categoria.objects.create(
        usuario=usuario,
        nome=nome
    )

def listar_por_usuario(usuario):
    return Categoria.objects.filter(usuario=usuario).order_by('nome')

def obter_por_id(id, usuario):
    return Categoria.objects.filter(id=id, usuario=usuario).first()

def atualizar(categoria, nome):
    categoria.nome = nome
    categoria.save()
    return categoria

def deletar(categoria):
    categoria.delete()