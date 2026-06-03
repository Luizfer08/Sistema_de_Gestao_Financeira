# SEGURANÇA
from django.contrib.auth.decorators import login_required

# JSON
from django.http import HttpResponse, JsonResponse

# RENDER
from django.shortcuts import render

# SERVICES
from financeiro.services.dashboard_service import (
    fim_do_mes,
    montar_dashboard
)

from financeiro.services.despesa_service import listar_despesas_por_periodo
from financeiro.services.receita_service import listar_receitas_por_periodo


def formatar_moeda(valor):

    return f"R$ {valor:.2f}".replace('.', ',')


def sim_nao(valor):

    return 'Sim' if valor else 'Nao'


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


def escapar_pdf(texto):

    texto = limpar_texto_pdf(texto)

    return (
        texto
        .replace('\\', '\\\\')
        .replace('(', '\\(')
        .replace(')', '\\)')
    )


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


def gerar_pdf_texto(linhas):

    linhas_por_pagina = 42
    paginas = [
        linhas[indice:indice + linhas_por_pagina]
        for indice in range(0, len(linhas), linhas_por_pagina)
    ] or [[]]

    objetos = []
    paginas_ids = []

    objetos.append('<< /Type /Catalog /Pages 2 0 R >>')
    objetos.append('')
    objetos.append(
        '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>'
    )

    for pagina in paginas:

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

    objetos[1] = (
        f"<< /Type /Pages /Kids "
        f"[{' '.join(f'{item} 0 R' for item in paginas_ids)}] "
        f"/Count {len(paginas_ids)} >>"
    )

    pdf = bytearray()
    pdf.extend(b'%PDF-1.4\n')
    offsets = []

    for indice, objeto in enumerate(objetos, start=1):
        offsets.append(len(pdf))
        pdf.extend(f'{indice} 0 obj\n'.encode('latin-1'))
        pdf.extend(objeto.encode('latin-1', errors='replace'))
        pdf.extend(b'\nendobj\n')

    xref_pos = len(pdf)
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


# DASHBOARD PRINCIPAL
@login_required
def dashboard(request):

    # Monta dados do dashboard com base no usuário e período selecionado
    dados = montar_dashboard(
        request.user,
        request.GET.get('mes'),
        request.GET.get('ano')
    )

    # Renderiza página do dashboard
    return render(
        request,
        'financeiro/dashboard.html',
        dados
    )


# API DE DADOS DO DASHBOARD
@login_required
def dashboard_dados(request):

    # Obtém dados atualizados do dashboard
    dados = montar_dashboard(
        request.user,
        request.GET.get('mes'),
        request.GET.get('ano')
    )

    # Resumo financeiro
    resumo = dados['resumo']

    # Retorna dados em formato JSON
    return JsonResponse({

        # Valores financeiros
        'saldo_atual': float(resumo['saldo_atual']),
        'saldo_futuro': float(resumo['saldo_futuro']),
        'receitas': float(resumo['receitas']),
        'despesas': float(resumo['despesas']),

        # Dados de variação percentual
        'variacoes': resumo['variacoes'],

        # Lista de notificações
        'notificacoes': dados['notificacoes'],

        # Dados do gráfico financeiro
        'grafico_financeiro': dados['grafico_financeiro'],

        # Dados das categorias
        'categorias': [
            {
                'nome': item['nome'],
                'tipo': item['tipo'],
                'cor': item['cor'],
                'total': float(item['total']),
            }

            # Percorre categorias retornadas pelo service
            for item in dados['categorias']
        ],

        # Mês e ano atual selecionado
        'mes': dados['mes_atual'].month,
        'ano': dados['mes_atual'].year,
    })


@login_required
def relatorio_mensal(request):

    dados = montar_dashboard(
        request.user,
        request.GET.get('mes'),
        request.GET.get('ano')
    )

    mes_atual = dados['mes_atual']
    fim = fim_do_mes(mes_atual)

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
            linhas.extend(
                quebrar_linha_pdf(
                    f"{notificacao['tipo']}: {notificacao['texto']}"
                )
            )

    else:
        linhas.append(
            'Nenhuma alteracao relevante em relacao ao mes anterior.'
        )

    nome_arquivo = (
        f"relatorio_financeiro_"
        f"{mes_atual.year}_{mes_atual.month:02d}.pdf"
    )

    response = HttpResponse(
        gerar_pdf_texto(linhas),
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="{nome_arquivo}"'
    )

    return response
