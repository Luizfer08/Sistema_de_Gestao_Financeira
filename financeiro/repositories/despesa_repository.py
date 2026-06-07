# Repository responsavel pelo acesso ao banco de dados de despesas.
from financeiro.models.despesa import Despesa
from financeiro.models.categoria import Categoria

# Funcoes de competencia controlam despesas fixas, parceladas e comuns.
from financeiro.competencia import (
    filtrar_por_competencia,
    somar_por_competencia
)

# Sum agrega valores diretamente no banco quando nao ha regra de competencia.
from django.db.models import Sum

# Datetime converte datas recebidas dos formularios.
from datetime import datetime


# Converte datas vindas do frontend para objeto date.
def converter_data(data_str):

    if not data_str:
        return None

    # Remove espacos extras antes de tentar converter.
    data_str = str(data_str).strip()

    # Aceita o formato do input date e tambem o formato brasileiro.
    for formato in ("%Y-%m-%d", "%d/%m/%Y"):

        try:

            return datetime.strptime(
                data_str,
                formato
            ).date()

        except ValueError:
            continue

    return None


# Converte valores numericos simples, usados na quantidade de parcelas.
def converter_inteiro(valor):

    if not valor:
        return None

    try:

        numero = int(valor)

        # Parcelas precisam ser sempre maiores que zero.
        return numero if numero > 0 else None

    except ValueError:

        return None


# Cria uma despesa a partir dos dados enviados pelo formulario.
def criar(usuario, data):

    # Data inicial da despesa ou da primeira parcela.
    data_lancamento = converter_data(
        data.get('data')
    )

    # Recorrente representa despesa fixa; parcelada representa despesa dividida.
    recorrente = True if data.get('recorrente') else False
    parcelada = True if data.get('parcelada') else False

    # Quantidade de competencias em que a despesa parcelada sera considerada.
    quantidade_parcelas = converter_inteiro(
        data.get('quantidade_parcelas')
    )

    # A data e obrigatoria para calcular o mes da despesa.
    if not data_lancamento:

        raise ValueError(
            "Data da despesa invalida"
        )

    # Uma despesa nao pode ser fixa e parcelada ao mesmo tempo.
    if recorrente and parcelada:

        raise ValueError(
            "Despesa fixa nao pode ser parcelada"
        )

    # Despesas parceladas precisam informar quantas parcelas existem.
    if parcelada and not quantidade_parcelas:

        raise ValueError(
            "Informe a quantidade de parcelas da despesa"
        )

    # Categoria e obrigatoria para organizar a despesa corretamente.
    if not data.get('categoria'):

        raise ValueError(
            "Informe a categoria da despesa"
        )

    # Busca somente categorias de despesa pertencentes ao usuario logado.
    try:

        categoria = Categoria.objects.get(
            id=data.get('categoria'),
            usuario=usuario,
            tipo=Categoria.TIPO_DESPESA
        )

    except Categoria.DoesNotExist:

        raise ValueError("Categoria invalida")

    # Salva a despesa no banco de dados.
    despesa = Despesa.objects.create(

        usuario=usuario,
        descricao=data.get('descricao'),
        valor=float(data.get('valor')),
        conta=data.get('conta') or '',
        data=data_lancamento,
        categoria=categoria,
        recorrente=recorrente,
        parcelada=parcelada,
        quantidade_parcelas=quantidade_parcelas,
        data_fim=converter_data(
            data.get('data_fim')
        )
    )

    return despesa


# Lista todas as despesas do usuario, da mais recente para a mais antiga.
def listar_por_usuario(usuario):

    return Despesa.objects.filter(
        usuario=usuario
    ).order_by('-data')


# Lista despesas que devem aparecer dentro do periodo selecionado.
def listar_por_periodo(usuario, data_inicio, data_fim):

    # Busca despesas criadas ate o final do mes.
    despesas = Despesa.objects.filter(
        usuario=usuario,
        data__lte=data_fim
    ).select_related('categoria')

    # Aplica a regra de competencia para fixas e parceladas.
    return filtrar_por_competencia(
        despesas,
        data_inicio
    )


# Busca uma despesa pelo id garantindo que ela pertence ao usuario.
def obter_por_id(id, usuario):

    return Despesa.objects.filter(
        id=id,
        usuario=usuario
    ).first()


# Atualiza uma despesa existente.
def atualizar(despesa, data):

    # Campos principais editaveis.
    despesa.descricao = data.get('descricao')

    if data.get('valor'):

        despesa.valor = float(
            data.get('valor')
        )

    # Conta e exclusiva das despesas.
    if 'conta' in data:

        despesa.conta = data.get('conta') or ''

    # Atualiza a data quando informada.
    if data.get('data'):

        data_lancamento = converter_data(
            data.get('data')
        )

        if not data_lancamento:

            raise ValueError(
                "Data da despesa invalida"
            )

        despesa.data = data_lancamento

    # Categoria e obrigatoria tambem na edicao.
    if not data.get('categoria'):

        raise ValueError(
            "Informe a categoria da despesa"
        )

    # Atualiza categoria mantendo a regra de tipo despesa.
    try:

        despesa.categoria = Categoria.objects.get(
            id=data.get('categoria'),
            usuario=despesa.usuario,
            tipo=Categoria.TIPO_DESPESA
        )

    except Categoria.DoesNotExist:

        raise ValueError(
            "Categoria invalida"
        )

    # Atualiza flags de recorrencia e parcelamento.
    despesa.recorrente = True if data.get('recorrente') else False
    despesa.parcelada = True if data.get('parcelada') else False

    # Mantem a regra de negocio: fixa e parcelada sao opcoes exclusivas.
    if despesa.recorrente and despesa.parcelada:

        raise ValueError(
            "Despesa fixa nao pode ser parcelada"
        )

    # Atualiza e valida a quantidade de parcelas.
    despesa.quantidade_parcelas = converter_inteiro(
        data.get('quantidade_parcelas')
    )

    if despesa.parcelada and not despesa.quantidade_parcelas:

        raise ValueError(
            "Informe a quantidade de parcelas da despesa"
        )

    # Mantem campo opcional para encerramento de recorrencia.
    despesa.data_fim = converter_data(
        data.get('data_fim')
    )

    despesa.save()

    return despesa


# Remove a despesa do banco de dados.
def deletar(despesa):

    despesa.delete()


# Soma todas as despesas cadastradas, sem filtro de competencia.
def somar_despesas(usuario):

    return Despesa.objects.filter(
        usuario=usuario
    ).aggregate(
        total=Sum('valor')
    )['total'] or 0


# Soma as despesas validas dentro de uma competencia.
def somar_despesas_por_periodo(usuario, data_inicio, data_fim):

    despesas = Despesa.objects.filter(
        usuario=usuario,
        data__lte=data_fim
    )

    return somar_por_competencia(
        despesas,
        data_inicio
    )
