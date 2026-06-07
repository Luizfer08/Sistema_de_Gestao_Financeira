from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from financeiro.competencia import ocorre_no_mes
from financeiro.models import Categoria, Despesa, Receita
from financeiro.services.categoria_service import listar_categorias
from financeiro.services.dashboard_service import montar_resumo_mensal
from financeiro.services.despesa_service import criar_despesa
from financeiro.services.receita_service import criar_receita


# Testes automatizados das principais regras de negocio do sistema financeiro.
class RegrasFinanceirasTestCase(TestCase):

    # Cria dados base utilizados nos testes.
    def setUp(self):

        self.usuario = User.objects.create_user(
            username='teste',
            email='teste@email.com',
            password='123456'
        )

        self.categoria_receita = Categoria.objects.create(
            usuario=self.usuario,
            nome='Salario',
            tipo=Categoria.TIPO_RECEITA,
            cor='#8FEBDD'
        )

        self.categoria_despesa = Categoria.objects.create(
            usuario=self.usuario,
            nome='Casa',
            tipo=Categoria.TIPO_DESPESA,
            cor='#5A4226'
        )

    # Receita deve exigir categoria para ser cadastrada.
    def test_receita_exige_categoria(self):

        with self.assertRaisesMessage(
            ValueError,
            'Informe a categoria da receita'
        ):
            criar_receita(self.usuario, {
                'descricao': 'Trabalho',
                'valor': '1000',
                'data': '2026-05-10',
            })

    # Despesa deve exigir categoria para ser cadastrada.
    def test_despesa_exige_categoria(self):

        with self.assertRaisesMessage(
            ValueError,
            'Informe a categoria da despesa'
        ):
            criar_despesa(self.usuario, {
                'descricao': 'Aluguel',
                'valor': '450',
                'data': '2026-05-10',
                'conta': 'Pix',
            })

    # Receita fixa nao pode ser parcelada ao mesmo tempo.
    def test_receita_fixa_nao_pode_ser_parcelada(self):

        with self.assertRaisesMessage(
            ValueError,
            'Receita fixa nao pode ser parcelada'
        ):
            criar_receita(self.usuario, {
                'descricao': 'Salario',
                'valor': '1000',
                'data': '2026-05-10',
                'categoria': self.categoria_receita.id,
                'recorrente': 'on',
                'parcelada': 'on',
                'quantidade_parcelas': '2',
            })

    # Despesa fixa nao pode ser parcelada ao mesmo tempo.
    def test_despesa_fixa_nao_pode_ser_parcelada(self):

        with self.assertRaisesMessage(
            ValueError,
            'Despesa fixa nao pode ser parcelada'
        ):
            criar_despesa(self.usuario, {
                'descricao': 'Internet',
                'valor': '120',
                'data': '2026-05-10',
                'categoria': self.categoria_despesa.id,
                'conta': 'Debito',
                'recorrente': 'on',
                'parcelada': 'on',
                'quantidade_parcelas': '2',
            })

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

    # Categorias de receita e despesa devem ser filtradas separadamente.
    def test_categorias_sao_filtradas_por_tipo(self):

        categorias_receita = listar_categorias(
            self.usuario,
            Categoria.TIPO_RECEITA
        )

        categorias_despesa = listar_categorias(
            self.usuario,
            Categoria.TIPO_DESPESA
        )

        self.assertIn(
            self.categoria_receita,
            categorias_receita
        )
        self.assertNotIn(
            self.categoria_despesa,
            categorias_receita
        )
        self.assertIn(
            self.categoria_despesa,
            categorias_despesa
        )
