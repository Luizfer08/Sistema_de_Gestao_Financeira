# Login_required protege dashboard e relatorio para usuarios autenticados.
from django.contrib.auth.decorators import login_required

# HttpResponse devolve o PDF; JsonResponse devolve dados para AJAX.
from django.http import HttpResponse, JsonResponse

# Render devolve a pagina HTML do dashboard.
from django.shortcuts import render

# Services montam resumo, graficos e dados financeiros.
from financeiro.services.dashboard_service import (
    fim_do_mes,
    montar_dashboard
)

from financeiro.services.despesa_service import listar_despesas_por_periodo
from financeiro.services.receita_service import listar_receitas_por_periodo


# Formata valores Decimais no padrao monetario brasileiro.
def formatar_moeda(valor):

    return f"R$ {valor:.2f}".replace('.', ',')


# Converte booleanos em texto usado no relatorio.
def sim_nao(valor):

    return 'Sim' if valor else 'Nao'


# Remove caracteres que podem quebrar a codificacao simples do PDF.
def limpar_texto_pdf(texto):

    texto = str(texto)

    substituicoes = {
        'ç': 'c',
        'Ç': 'C',
        'ã': 'a',
        'Ã': 'A',
        'á': 'a',
        'Á': 'A',
        'â': 'a',
        'Â': 'A',
        'à': 'a',
        'À': 'A',
        'é': 'e',
        'É': 'E',
        'ê': 'e',
        'Ê': 'E',
        'í': 'i',
        'Í': 'I',
        'ó': 'o',
        'Ó': 'O',
        'ô': 'o',
        'Ô': 'O',
        'õ': 'o',
        'Õ': 'O',
        'ú': 'u',
        'Ú': 'U',
    }

    for original, novo in substituicoes.items():
        texto = texto.replace(original, novo)

    return texto


# Escapa caracteres especiais antes de escrever no PDF.
def escapar_pdf(texto):

    texto = limpar_texto_pdf(texto)

    return (
        texto
        .replace('\\', '\\\\')
        .replace('(', '\\(')
        .replace(')', '\\)')
    )


# Divide textos longos para caberem dentro da largura da pagina do PDF.
def quebrar_linha_pdf(texto, limite=94):

    palavras = limpar_texto_pdf(texto).split()
    linhas = []
    linha_atual = ''

    for palavra in palavras:

        candidato = (
            f"{linha_atual} {palavra}".strip()
        )

        if len(candidato) <= limite:
            linha_atual = candidato
        else:
            if linha_atual:
                linhas.append(linha_atual)
            linha_atual = palavra

    if linha_atual:
        linhas.append(linha_atual)

    return linhas or ['']


# Gera um PDF simples em memoria, sem depender de biblioteca externa.
def gerar_pdf_texto(linhas):

    # Limite de linhas para manter o conteudo dentro da pagina.
    linhas_por_pagina = 42
    paginas = [
        linhas[indice:indice + linhas_por_pagina]
        for indice in range(0, len(linhas), linhas_por_pagina)
    ] or [[]]

    objetos = []
    paginas_ids = []

    # Objetos iniciais do documento PDF: catalogo, paginas e fonte.
    objetos.append('<< /Type /Catalog /Pages 2 0 R >>')
    objetos.append('')
    objetos.append(
        '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>'
    )

    for pagina in paginas:

        # Comandos de texto usados pelo formato PDF.
        conteudo = [
            'BT',
            '/F1 11 Tf',
            '50 790 Td',
            '14 TL',
        ]

        for linha in pagina:
            conteudo.append(f"({escapar_pdf(linha)}) Tj")
            conteudo.append('T*')

        conteudo.append('ET')

        # Cada pagina recebe um stream de conteudo e um objeto Page.
        stream = '\n'.join(conteudo)
        conteudo_id = len(objetos) + 1
        pagina_id = conteudo_id + 1

        objetos.append(
            f"<< /Length {len(stream.encode('latin-1', errors='replace'))} >>\n"
            f"stream\n{stream}\nendstream"
        )

        objetos.append(
            f"<< /Type /Page /Parent 2 0 R "
            f"/MediaBox [0 0 595 842] "
            f"/Resources << /Font << /F1 3 0 R >> >> "
            f"/Contents {conteudo_id} 0 R >>"
        )

        paginas_ids.append(pagina_id)

    # Atualiza o objeto de paginas com todos os ids gerados.
    objetos[1] = (
        f"<< /Type /Pages /Kids "
        f"[{' '.join(f'{item} 0 R' for item in paginas_ids)}] "
        f"/Count {len(paginas_ids)} >>"
    )

    pdf = bytearray()
    pdf.extend(b'%PDF-1.4\n')
    offsets = []

    # Escreve os objetos do PDF e registra suas posicoes.
    for indice, objeto in enumerate(objetos, start=1):
        offsets.append(len(pdf))
        pdf.extend(f'{indice} 0 obj\n'.encode('latin-1'))
        pdf.extend(objeto.encode('latin-1', errors='replace'))
        pdf.extend(b'\nendobj\n')

    xref_pos = len(pdf)

    # Xref e trailer finalizam a estrutura do arquivo PDF.
    pdf.extend(f'xref\n0 {len(objetos) + 1}\n'.encode('latin-1'))
    pdf.extend(b'0000000000 65535 f \n')

    for offset in offsets:
        pdf.extend(f'{offset:010d} 00000 n \n'.encode('latin-1'))

    pdf.extend(
        (
            f'trailer\n<< /Size {len(objetos) + 1} /Root 1 0 R >>\n'
            f'startxref\n{xref_pos}\n%%EOF'
        ).encode('latin-1')
    )

    return bytes(pdf)


# Renderiza o dashboard principal.
@login_required
def dashboard(request):

    # Monta dados com base no usuario e no mes selecionado.
    dados = montar_dashboard(
        request.user,
        request.GET.get('mes'),
        request.GET.get('ano')
    )

    # Envia os dados para o template HTML.
    return render(
        request,
        'financeiro/dashboard.html',
        dados
    )


# API que devolve os dados do dashboard em JSON.
@login_required
def dashboard_dados(request):

    # Monta o mesmo conjunto de dados usado pela tela.
    dados = montar_dashboard(
        request.user,
        request.GET.get('mes'),
        request.GET.get('ano')
    )

    # Resumo financeiro usado nos cards.
    resumo = dados['resumo']

    # Retorna dados convertidos para tipos aceitos em JSON.
    return JsonResponse({

        # Valores financeiros dos cards.
        'saldo_atual': float(resumo['saldo_atual']),
        'saldo_futuro': float(resumo['saldo_futuro']),
        'receitas': float(resumo['receitas']),
        'despesas': float(resumo['despesas']),

        # Variacoes percentuais dos cards.
        'variacoes': resumo['variacoes'],

        # Notificacoes do dashboard.
        'notificacoes': dados['notificacoes'],

        # Dados do grafico financeiro.
        'grafico_financeiro': dados['grafico_financeiro'],

        # Dados do grafico de categorias.
        'categorias': [
            {
                'nome': item['nome'],
                'tipo': item['tipo'],
                'cor': item['cor'],
                'total': float(item['total']),
            }

            # Converte Decimal para float em cada categoria.
            for item in dados['categorias']
        ],

        # Mes e ano selecionados na tela.
        'mes': dados['mes_atual'].month,
        'ano': dados['mes_atual'].year,
    })


# Gera e baixa o relatorio financeiro mensal em PDF.
@login_required
def relatorio_mensal(request):

    # Reaproveita os mesmos dados do dashboard para manter consistencia.
    dados = montar_dashboard(
        request.user,
        request.GET.get('mes'),
        request.GET.get('ano')
    )

    # Define a competencia do relatorio.
    mes_atual = dados['mes_atual']
    fim = fim_do_mes(mes_atual)

    # Lista movimentacoes validas para o mes selecionado.
    receitas = listar_receitas_por_periodo(
        request.user,
        mes_atual,
        fim
    )

    despesas = listar_despesas_por_periodo(
        request.user,
        mes_atual,
        fim
    )

    resumo = dados['resumo']

    # Linhas iniciais do relatorio.
    linhas = [
        'RELATORIO FINANCEIRO MENSAL',
        f"Usuario: {request.user.username}",
        f"Competencia: {dados['mes_nome']} / {mes_atual.year}",
        '',
        'RESUMO',
        f"Saldo atual: {formatar_moeda(resumo['saldo_atual'])}",
        f"Saldo futuro: {formatar_moeda(resumo['saldo_futuro'])}",
        f"Total de receitas: {formatar_moeda(resumo['receitas'])}",
        f"Total de despesas: {formatar_moeda(resumo['despesas'])}",
        '',
        'RECEITAS',
    ]

    for receita in receitas:
        # Cada receita vira uma linha textual no PDF.
        linha = (
            f"{receita.data.strftime('%d/%m/%Y')} | "
            f"{receita.descricao} | "
            f"{receita.categoria.nome if receita.categoria else 'Sem categoria'} | "
            f"Fixa: {sim_nao(receita.recorrente)} | "
            f"Parcelada: {sim_nao(receita.parcelada)} | "
            f"Parcelas: {receita.quantidade_parcelas or '-'} | "
            f"{formatar_moeda(receita.valor)}"
        )
        linhas.extend(quebrar_linha_pdf(linha))

    if not receitas:
        linhas.append('Nenhuma receita cadastrada nesta competencia.')

    linhas.extend([
        '',
        'DESPESAS',
    ])

    for despesa in despesas:
        # Cada despesa vira uma linha textual no PDF.
        linha = (
            f"{despesa.data.strftime('%d/%m/%Y')} | "
            f"{despesa.descricao} | "
            f"{despesa.categoria.nome if despesa.categoria else 'Sem categoria'} | "
            f"Conta: {despesa.conta or '-'} | "
            f"Fixa: {sim_nao(despesa.recorrente)} | "
            f"Parcelada: {sim_nao(despesa.parcelada)} | "
            f"Parcelas: {despesa.quantidade_parcelas or '-'} | "
            f"{formatar_moeda(despesa.valor)}"
        )
        linhas.extend(quebrar_linha_pdf(linha))

    if not despesas:
        linhas.append('Nenhuma despesa cadastrada nesta competencia.')

    linhas.extend([
        '',
        'CATEGORIAS',
    ])

    for categoria in dados['categorias']:
        # Categorias mostram totais consolidados por tipo.
        linhas.append(
            f"{categoria['nome']} | {categoria['tipo']} | "
            f"{formatar_moeda(categoria['total'])}"
        )

    linhas.extend([
        '',
        'NOTIFICACOES',
    ])

    if dados['notificacoes']:

        for notificacao in dados['notificacoes']:
            # Notificacoes longas sao quebradas para caber na pagina.
            linhas.extend(
                quebrar_linha_pdf(
                    f"{notificacao['tipo']}: {notificacao['texto']}"
                )
            )

    else:
        linhas.append(
            'Nenhuma alteracao relevante em relacao ao mes anterior.'
        )

    # Nome do arquivo inclui ano e mes da competencia.
    nome_arquivo = (
        f"relatorio_financeiro_"
        f"{mes_atual.year}_{mes_atual.month:02d}.pdf"
    )

    # Cria a resposta HTTP que forca o download do PDF.
    response = HttpResponse(
        gerar_pdf_texto(linhas),
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="{nome_arquivo}"'
    )

    return response
