from datetime import date
from decimal import Decimal

from financeiro.competencia import (
    filtrar_por_competencia,
    ocorre_no_mes,
    somar_por_competencia
)
from financeiro.models import Despesa, Receita
from financeiro.tests.base import FinanceiroTestCase


# Testa as regras de competencia usadas por receitas e despesas.
class CompetenciaTestCase(FinanceiroTestCase):

    # Lancamento fixo deve continuar aparecendo nos meses seguintes.
    def test_lancamento_fixo_aparece_nos_meses_seguintes(self):

        receita = Receita.objects.create(
            usuario=self.usuario,
            descricao='Salario fixo',
            valor=Decimal('1000.00'),
            data=date(2026, 5, 10),
            categoria=self.categoria_receita,
            recorrente=True
        )

        self.assertTrue(
            ocorre_no_mes(receita, date(2026, 6, 1))
        )

    # Lancamento parcelado deve aparecer apenas ate terminar as parcelas.
    def test_lancamento_parcelado_respeita_quantidade_de_parcelas(self):

        despesa = Despesa.objects.create(
            usuario=self.usuario,
            descricao='Compra parcelada',
            valor=Decimal('200.00'),
            data=date(2026, 5, 10),
            categoria=self.categoria_despesa,
            conta='Credito',
            parcelada=True,
            quantidade_parcelas=2
        )

        self.assertTrue(
            ocorre_no_mes(despesa, date(2026, 5, 1))
        )
        self.assertTrue(
            ocorre_no_mes(despesa, date(2026, 6, 1))
        )
        self.assertFalse(
            ocorre_no_mes(despesa, date(2026, 7, 1))
        )

    # Lancamento comum deve aparecer somente no mes em que foi criado.
    def test_lancamento_comum_aparece_apenas_no_mes_original(self):

        receita = Receita.objects.create(
            usuario=self.usuario,
            descricao='Freelance',
            valor=Decimal('300.00'),
            data=date(2026, 5, 20),
            categoria=self.categoria_receita
        )

        self.assertTrue(
            ocorre_no_mes(receita, date(2026, 5, 1))
        )
        self.assertFalse(
            ocorre_no_mes(receita, date(2026, 6, 1))
        )

    # Filtro de competencia retorna apenas itens validos e ordenados.
    def test_filtrar_por_competencia_ordena_por_data_e_descricao(self):

        Receita.objects.create(
            usuario=self.usuario,
            descricao='Zeta',
            valor=Decimal('100.00'),
            data=date(2026, 5, 20),
            categoria=self.categoria_receita
        )
        Receita.objects.create(
            usuario=self.usuario,
            descricao='Alpha',
            valor=Decimal('200.00'),
            data=date(2026, 5, 10),
            categoria=self.categoria_receita
        )
        Receita.objects.create(
            usuario=self.usuario,
            descricao='Fora do mes',
            valor=Decimal('500.00'),
            data=date(2026, 6, 1),
            categoria=self.categoria_receita
        )

        receitas = filtrar_por_competencia(
            Receita.objects.filter(usuario=self.usuario),
            date(2026, 5, 1)
        )

        self.assertEqual(
            [receita.descricao for receita in receitas],
            ['Alpha', 'Zeta']
        )

    # Soma de competencia considera fixas, parceladas e comuns validas no mes.
    def test_somar_por_competencia_soma_apenas_itens_validos(self):

        Receita.objects.create(
            usuario=self.usuario,
            descricao='Comum',
            valor=Decimal('100.00'),
            data=date(2026, 5, 10),
            categoria=self.categoria_receita
        )
        Receita.objects.create(
            usuario=self.usuario,
            descricao='Fixa',
            valor=Decimal('500.00'),
            data=date(2026, 4, 10),
            categoria=self.categoria_receita,
            recorrente=True
        )

        total = somar_por_competencia(
            Receita.objects.filter(usuario=self.usuario),
            date(2026, 5, 1)
        )

        self.assertEqual(
            total,
            Decimal('600.00')
        )
