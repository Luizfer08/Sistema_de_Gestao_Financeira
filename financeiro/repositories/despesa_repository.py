# MODELS
from financeiro.models.despesa import Despesa
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


# CRIAR DESPESA
def criar(usuario, data):

    # Converte data de lançamento
    data_lancamento = converter_data(
        data.get('data')
    )

    # Define se despesa é parcelada
    parcelada = True if data.get('parcelada') else False

    # Obtém quantidade de parcelas
    quantidade_parcelas = converter_inteiro(
        data.get('quantidade_parcelas')
    )

    # Valida data
    if not data_lancamento:

        raise ValueError(
            "Data da despesa invalida"
        )

    # Valida parcelamento
    if parcelada and not quantidade_parcelas:

        raise ValueError(
            "Informe a quantidade de parcelas da despesa"
        )

    # Busca categoria
    categoria = None

    if data.get('categoria'):

        try:

            categoria = Categoria.objects.get(
                id=data.get('categoria'),
                usuario=usuario,
                tipo=Categoria.TIPO_DESPESA
            )

        except Categoria.DoesNotExist:

            raise ValueError("Categoria inválida")

    # Cria despesa
    despesa = Despesa.objects.create(

        # Usuário dono da despesa
        usuario=usuario,

        # Dados principais
        descricao=data.get('descricao'),

        valor=float(data.get('valor')),

        # Conta vinculada
        conta=data.get('conta') or '',

        # Data principal
        data=data_lancamento,

        # Categoria
        categoria=categoria,

        # Configurações financeiras
        recorrente=True if data.get('recorrente') else False,

        parcelada=parcelada,

        quantidade_parcelas=quantidade_parcelas,

        # Data final de recorrência
        data_fim=converter_data(
            data.get('data_fim')
        )
    )

    return despesa


# LISTAR TODAS AS DESPESAS
def listar_por_usuario(usuario):

    return Despesa.objects.filter(
        usuario=usuario
    ).order_by('-data')


# LISTAR DESPESAS POR PERÍODO
def listar_por_periodo(usuario, data_inicio, data_fim):

    # Busca despesas até data final
    despesas = Despesa.objects.filter(
        usuario=usuario,
        data__lte=data_fim
    ).select_related('categoria')

    # Filtra despesas válidas na competência
    return filtrar_por_competencia(
        despesas,
        data_inicio
    )


# BUSCA DESPESA PELO ID
def obter_por_id(id, usuario):

    return Despesa.objects.filter(
        id=id,
        usuario=usuario
    ).first()


# ATUALIZAR DESPESA
def atualizar(despesa, data):

    # Atualiza descrição
    despesa.descricao = data.get('descricao')

    # Atualiza valor
    if data.get('valor'):

        despesa.valor = float(
            data.get('valor')
        )

    # Atualiza conta
    if 'conta' in data:

        despesa.conta = data.get('conta') or ''

    # Atualiza data
    if data.get('data'):

        data_lancamento = converter_data(
            data.get('data')
        )

        if not data_lancamento:

            raise ValueError(
                "Data da despesa invalida"
            )

        despesa.data = data_lancamento

    # Atualiza categoria
    if data.get('categoria'):

        try:

            despesa.categoria = Categoria.objects.get(
                id=data.get('categoria'),
                usuario=despesa.usuario,
                tipo=Categoria.TIPO_DESPESA
            )

        except Categoria.DoesNotExist:

            raise ValueError(
                "Categoria inválida"
            )

    # Atualiza recorrência
    despesa.recorrente = True if data.get('recorrente') else False

    # Atualiza parcelamento
    despesa.parcelada = True if data.get('parcelada') else False

    # Atualiza quantidade de parcelas
    despesa.quantidade_parcelas = converter_inteiro(
        data.get('quantidade_parcelas')
    )

    # Valida parcelamento
    if despesa.parcelada and not despesa.quantidade_parcelas:

        raise ValueError(
            "Informe a quantidade de parcelas da despesa"
        )

    # Atualiza data final
    despesa.data_fim = converter_data(
        data.get('data_fim')
    )

    # Salva alterações
    despesa.save()

    return despesa


# DELETAR DESPESA
def deletar(despesa):

    despesa.delete()


# SOMA TOTAL DAS DESPESAS
def somar_despesas(usuario):

    return Despesa.objects.filter(
        usuario=usuario
    ).aggregate(
        total=Sum('valor')
    )['total'] or 0


# SOMA DESPESAS POR PERÍODO
def somar_despesas_por_periodo(usuario, data_inicio, data_fim):

    # Busca despesas até data final
    despesas = Despesa.objects.filter(
        usuario=usuario,
        data__lte=data_fim
    )

    # Soma despesas válidas da competência
    return somar_por_competencia(
        despesas,
        data_inicio
    )