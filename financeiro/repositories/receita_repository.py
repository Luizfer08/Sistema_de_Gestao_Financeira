# MODELS
from financeiro.models import Receita
from financeiro.models.categoria import Categoria

# COMPETÊNCIA FINANCEIRA
from financeiro.competencia import (
    filtrar_por_competencia,
    somar_por_competencia
)

# AGREGAÇÃO
from django.db.models import Sum

# DATAS
from datetime import datetime


# CONVERTE STRING PARA DATA
def converter_data(data_str):

    """
    Converte string para objeto date

    Aceita:
    - YYYY-MM-DD
    - DD/MM/YYYY
    """

    if not data_str:
        return None

    # Remove espaços extras
    data_str = str(data_str).strip()

    # Tenta converter utilizando formatos disponíveis
    for formato in ("%Y-%m-%d", "%d/%m/%Y"):

        try:

            return datetime.strptime(
                data_str,
                formato
            ).date()

        except ValueError:
            continue

    return None


# CONVERTE VALOR PARA INTEIRO
def converter_inteiro(valor):

    if not valor:
        return None

    try:

        numero = int(valor)

        # Retorna apenas números positivos
        return numero if numero > 0 else None

    except ValueError:

        return None


# CRIAR RECEITA
def criar(usuario, data):

    # Converte data de lançamento
    data_lancamento = converter_data(
        data.get('data')
    )

    # Define se receita é parcelada
    recorrente = True if data.get('recorrente') else False

    parcelada = True if data.get('parcelada') else False

    # Obtém quantidade de parcelas
    quantidade_parcelas = converter_inteiro(
        data.get('quantidade_parcelas')
    )

    # Valida data
    if not data_lancamento:

        raise ValueError(
            "Data da receita invalida"
        )

    # Valida parcelamento
    if recorrente and parcelada:

        raise ValueError(
            "Receita fixa nao pode ser parcelada"
        )

    if parcelada and not quantidade_parcelas:

        raise ValueError(
            "Informe a quantidade de parcelas da receita"
        )

    # Busca categoria
    categoria = None

    if data.get('categoria'):

        try:

            categoria = Categoria.objects.get(
                id=data.get('categoria'),
                usuario=usuario,
                tipo=Categoria.TIPO_RECEITA
            )

        except Categoria.DoesNotExist:

            raise ValueError(
                "Categoria inválida"
            )

    # Cria receita
    receita = Receita.objects.create(

        # Usuário dono da receita
        usuario=usuario,

        # Dados principais
        descricao=data.get('descricao'),

        valor=float(data.get('valor')),

        # Data principal
        data=data_lancamento,

        # Categoria
        categoria=categoria,

        # Configurações financeiras
        recorrente=recorrente,

        parcelada=parcelada,

        quantidade_parcelas=quantidade_parcelas,

        # Data final da recorrência
        data_fim=converter_data(
            data.get('data_fim')
        )
    )

    return receita


# LISTAR TODAS AS RECEITAS
def listar_por_usuario(usuario):

    return Receita.objects.filter(
        usuario=usuario
    ).order_by('-data')


# LISTAR RECEITAS POR PERÍODO
def listar_por_periodo(usuario, data_inicio, data_fim):

    # Busca receitas até data final
    receitas = Receita.objects.filter(
        usuario=usuario,
        data__lte=data_fim
    ).select_related('categoria')

    # Filtra receitas válidas na competência
    return filtrar_por_competencia(
        receitas,
        data_inicio
    )


# BUSCA RECEITA PELO ID
def obter_por_id(id, usuario):

    return Receita.objects.filter(
        id=id,
        usuario=usuario
    ).first()


# ATUALIZAR RECEITA
def atualizar(receita, data):

    # Atualiza descrição
    receita.descricao = data.get('descricao')

    # Atualiza valor
    if data.get('valor'):

        receita.valor = float(
            data.get('valor')
        )

    # Atualiza data
    if data.get('data'):

        data_lancamento = converter_data(
            data.get('data')
        )

        if not data_lancamento:

            raise ValueError(
                "Data da receita invalida"
            )

        receita.data = data_lancamento

    # Atualiza categoria
    if data.get('categoria'):

        try:

            receita.categoria = Categoria.objects.get(
                id=data.get('categoria'),
                usuario=receita.usuario,
                tipo=Categoria.TIPO_RECEITA
            )

        except Categoria.DoesNotExist:

            raise ValueError(
                "Categoria inválida"
            )

    # Atualiza recorrência
    receita.recorrente = True if data.get('recorrente') else False

    # Atualiza parcelamento
    receita.parcelada = True if data.get('parcelada') else False

    if receita.recorrente and receita.parcelada:

        raise ValueError(
            "Receita fixa nao pode ser parcelada"
        )

    # Atualiza quantidade de parcelas
    receita.quantidade_parcelas = converter_inteiro(
        data.get('quantidade_parcelas')
    )

    # Valida parcelamento
    if receita.parcelada and not receita.quantidade_parcelas:

        raise ValueError(
            "Informe a quantidade de parcelas da receita"
        )

    # Atualiza data final
    receita.data_fim = converter_data(
        data.get('data_fim')
    )

    # Salva alterações
    receita.save()

    return receita


# DELETAR RECEITA
def deletar(receita):

    receita.delete()


# SOMA TOTAL DAS RECEITAS
def somar_receitas(usuario):

    return Receita.objects.filter(
        usuario=usuario
    ).aggregate(
        total=Sum('valor')
    )['total'] or 0


# SOMA RECEITAS POR PERÍODO
def somar_receitas_por_periodo(usuario, data_inicio, data_fim):

    # Busca receitas até data final
    receitas = Receita.objects.filter(
        usuario=usuario,
        data__lte=data_fim
    )

    # Soma receitas válidas da competência
    return somar_por_competencia(
        receitas,
        data_inicio
    )
