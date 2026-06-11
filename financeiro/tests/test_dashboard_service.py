from datetime import date
from decimal import Decimal

from financeiro.models import Despesa, Receita
from financeiro.services.dashboard_service import (
    calcular_variacao,
    montar_categorias,
    montar_dashboard,
    montar_historico_financeiro,
    montar_resumo_mensal,
    montar_ultimas_transacoes,
    obter_mes_referencia,
    somar_mes
)
from financeiro.tests.base import FinanceiroTestCase


# Testa os calculos e estruturas usados pelo dashboard.
class DashboardServiceTestCase(FinanceiroTestCase):

    # Saldo futuro deve usar o mes seguinte ao mes selecionado.
    def test_saldo_futuro_considera_proximo_mes(self):

        Receita.objects.create(
            usuario=self.usuario,
            descricao='Receita de maio',
            valor=Decimal('1000.00'),
            data=date(2026, 5, 10),
            categoria=self.categoria_receita
        )

        Receita.objects.create(
            usuario=self.usuario,
            descricao='Receita fixa',
            valor=Decimal('500.00'),
            data=date(2026, 5, 10),
            categoria=self.categoria_receita,
            recorrente=True
        )

        Despesa.objects.create(
            usuario=self.usuario,
            descricao='Despesa parcelada',
            valor=Decimal('200.00'),
            data=date(2026, 5, 10),
            categoria=self.categoria_despesa,
            conta='Pix',
            parcelada=True,
            quantidade_parcelas=2
        )

        resumo = montar_resumo_mensal(
            self.usuario,
            date(2026, 5, 1)
        )

        self.assertEqual(
            resumo['saldo_atual'],
            Decimal('1300.00')
        )
        self.assertEqual(
            resumo['saldo_futuro'],
            Decimal('300.00')
        )

    # Variacao deve indicar alta, baixa e estabilidade.
    def test_calcular_variacao_retorna_direcoes_corretas(self):

        self.assertEqual(
            calcular_variacao(Decimal('200'), Decimal('100'))['direcao'],
            'up'
        )
        self.assertEqual(
            calcular_variacao(Decimal('50'), Decimal('100'))['direcao'],
            'down'
        )
        self.assertEqual(
            calcular_variacao(Decimal('100'), Decimal('100'))['direcao'],
            'same'
        )

    # Soma de meses deve virar ano quando necessario.
    def test_somar_mes_ajusta_virada_de_ano(self):

        self.assertEqual(
            somar_mes(date(2026, 12, 1), 1),
            date(2027, 1, 1)
        )
        self.assertEqual(
            somar_mes(date(2026, 1, 1), -1),
            date(2025, 12, 1)
        )

    # Mes invalido na URL deve voltar para o mes atual.
    def test_obter_mes_referencia_trata_valor_invalido(self):

        referencia = obter_mes_referencia(
            'abc',
            '2026'
        )

        self.assertEqual(
            referencia.day,
            1
        )

    # Grafico historico deve montar labels e series financeiras.
    def test_montar_historico_financeiro_retorna_series(self):

        Receita.objects.create(
            usuario=self.usuario,
            descricao='Receita',
            valor=Decimal('100.00'),
            data=date(2026, 5, 10),
            categoria=self.categoria_receita
        )

        historico = montar_historico_financeiro(
            self.usuario,
            date(2026, 5, 1),
            quantidade=2
        )

        self.assertEqual(
            len(historico['labels']),
            2
        )
        self.assertEqual(
            historico['receitas'][-1],
            100.0
        )

    # Grafico de categorias deve somar receitas e despesas da competencia.
    def test_montar_categorias_retorna_totais_por_categoria(self):

        Receita.objects.create(
            usuario=self.usuario,
            descricao='Receita',
            valor=Decimal('100.00'),
            data=date(2026, 5, 10),
            categoria=self.categoria_receita
        )
        Despesa.objects.create(
            usuario=self.usuario,
            descricao='Despesa',
            valor=Decimal('50.00'),
            data=date(2026, 5, 10),
            categoria=self.categoria_despesa,
            conta='Pix'
        )

        categorias = montar_categorias(
            self.usuario,
            date(2026, 5, 1)
        )

        totais = {
            item['nome']: item['total']
            for item in categorias
        }

        self.assertEqual(
            totais['Salario'],
            Decimal('100.00')
        )
        self.assertEqual(
            totais['Casa'],
            Decimal('50.00')
        )

    # Ultimas transacoes deve misturar receitas e despesas recentes.
    def test_montar_ultimas_transacoes_retorna_receitas_e_despesas(self):

        Receita.objects.create(
            usuario=self.usuario,
            descricao='Receita',
            valor=Decimal('100.00'),
            data=date(2026, 5, 10),
            categoria=self.categoria_receita
        )
        Despesa.objects.create(
            usuario=self.usuario,
            descricao='Despesa',
            valor=Decimal('50.00'),
            data=date(2026, 5, 10),
            categoria=self.categoria_despesa,
            conta='Pix'
        )

        transacoes = montar_ultimas_transacoes(
            self.usuario,
            limite=5
        )

        tipos = {
            item['tipo']
            for item in transacoes
        }

        self.assertEqual(
            tipos,
            {'receita', 'despesa'}
        )

    # Dashboard completo deve retornar todos os blocos consumidos pela tela.
    def test_montar_dashboard_retorna_blocos_principais(self):

        dashboard = montar_dashboard(
            self.usuario,
            5,
            2026
        )

        self.assertIn(
            'resumo',
            dashboard
        )
        self.assertIn(
            'grafico_financeiro',
            dashboard
        )
        self.assertIn(
            'notificacoes',
            dashboard
        )
