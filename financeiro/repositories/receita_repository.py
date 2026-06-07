# Repository responsavel pelo acesso ao banco de dados de receitas.
from financeiro.models import Receita
from financeiro.models.categoria import Categoria

# Funcoes de competencia controlam receitas fixas, parceladas e comuns.
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


# Cria uma receita a partir dos dados enviados pelo formulario.
def criar(usuario, data):

    # Data inicial da receita ou da primeira parcela.
    data_lancamento = converter_data(
        data.get('data')
    )

    # Recorrente representa renda fixa; parcelada representa renda dividida.
    recorrente = True if data.get('recorrente') else False
    parcelada = True if data.get('parcelada') else False

    # Quantidade de competencias em que a receita parcelada sera considerada.
    quantidade_parcelas = converter_inteiro(
        data.get('quantidade_parcelas')
    )

    # A data e obrigatoria para calcular o mes da receita.
    if not data_lancamento:

        raise ValueError(
            "Data da receita invalida"
        )

    # Uma receita nao pode ser fixa e parcelada ao mesmo tempo.
    if recorrente and parcelada:

        raise ValueError(
            "Receita fixa nao pode ser parcelada"
        )

    # Receitas parceladas precisam informar quantas parcelas existem.
    if parcelada and not quantidade_parcelas:

        raise ValueError(
            "Informe a quantidade de parcelas da receita"
        )

    # Categoria e obrigatoria para organizar a receita corretamente.
    if not data.get('categoria'):

        raise ValueError(
            "Informe a categoria da receita"
        )

    # Busca somente categorias de receita pertencentes ao usuario logado.
    try:

        categoria = Categoria.objects.get(
            id=data.get('categoria'),
            usuario=usuario,
            tipo=Categoria.TIPO_RECEITA
        )

    except Categoria.DoesNotExist:

        raise ValueError(
            "Categoria invalida"
        )

    # Salva a receita no banco de dados.
    receita = Receita.objects.create(

        usuario=usuario,
        descricao=data.get('descricao'),
        valor=float(data.get('valor')),
        data=data_lancamento,
        categoria=categoria,
        recorrente=recorrente,
        parcelada=parcelada,
        quantidade_parcelas=quantidade_parcelas,
        data_fim=converter_data(
            data.get('data_fim')
        )
    )

    return receita


# Lista todas as receitas do usuario, da mais recente para a mais antiga.
def listar_por_usuario(usuario):

    return Receita.objects.filter(
        usuario=usuario
    ).order_by('-data')


# Lista receitas que devem aparecer dentro do periodo selecionado.
def listar_por_periodo(usuario, data_inicio, data_fim):

    # Busca receitas criadas ate o final do mes.
    receitas = Receita.objects.filter(
        usuario=usuario,
        data__lte=data_fim
    ).select_related('categoria')

    # Aplica a regra de competencia para fixas e parceladas.
    return filtrar_por_competencia(
        receitas,
        data_inicio
    )


# Busca uma receita pelo id garantindo que ela pertence ao usuario.
def obter_por_id(id, usuario):

    return Receita.objects.filter(
        id=id,
        usuario=usuario
    ).first()


# Atualiza uma receita existente.
def atualizar(receita, data):

    # Campos principais editaveis.
    receita.descricao = data.get('descricao')

    if data.get('valor'):

        receita.valor = float(
            data.get('valor')
        )

    # Atualiza a data quando informada.
    if data.get('data'):

        data_lancamento = converter_data(
            data.get('data')
        )

        if not data_lancamento:

            raise ValueError(
                "Data da receita invalida"
            )

        receita.data = data_lancamento

    # Categoria e obrigatoria tambem na edicao.
    if not data.get('categoria'):

        raise ValueError(
            "Informe a categoria da receita"
        )

    # Atualiza categoria mantendo a regra de tipo receita.
    try:

        receita.categoria = Categoria.objects.get(
            id=data.get('categoria'),
            usuario=receita.usuario,
            tipo=Categoria.TIPO_RECEITA
        )

    except Categoria.DoesNotExist:

        raise ValueError(
            "Categoria invalida"
        )

    # Atualiza flags de recorrencia e parcelamento.
    receita.recorrente = True if data.get('recorrente') else False
    receita.parcelada = True if data.get('parcelada') else False

    # Mantem a regra de negocio: fixa e parcelada sao opcoes exclusivas.
    if receita.recorrente and receita.parcelada:

        raise ValueError(
            "Receita fixa nao pode ser parcelada"
        )

    # Atualiza e valida a quantidade de parcelas.
    receita.quantidade_parcelas = converter_inteiro(
        data.get('quantidade_parcelas')
    )

    if receita.parcelada and not receita.quantidade_parcelas:

        raise ValueError(
            "Informe a quantidade de parcelas da receita"
        )

    # Mantem campo opcional para encerramento de recorrencia.
    receita.data_fim = converter_data(
        data.get('data_fim')
    )

    receita.save()

    return receita


# Remove a receita do banco de dados.
def deletar(receita):

    receita.delete()


# Soma todas as receitas cadastradas, sem filtro de competencia.
def somar_receitas(usuario):

    return Receita.objects.filter(
        usuario=usuario
    ).aggregate(
        total=Sum('valor')
    )['total'] or 0


# Soma as receitas validas dentro de uma competencia.
def somar_receitas_por_periodo(usuario, data_inicio, data_fim):

    receitas = Receita.objects.filter(
        usuario=usuario,
        data__lte=data_fim
    )

    return somar_por_competencia(
        receitas,
        data_inicio
    )
