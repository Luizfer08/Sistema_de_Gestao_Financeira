from datetime import date
from decimal import Decimal

from financeiro.models import Despesa
from financeiro.services.despesa_service import (
    criar_despesa,
    editar_despesa,
    excluir_despesa,
    listar_despesas_por_periodo
)
from financeiro.tests.base import FinanceiroTestCase


# Testa as regras de negocio ligadas ao cadastro de despesas.
class DespesaServiceTestCase(FinanceiroTestCase):

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

    # Despesa parcelada precisa informar quantidade de parcelas.
    def test_despesa_parcelada_exige_quantidade_de_parcelas(self):

        with self.assertRaisesMessage(
            ValueError,
            'Informe a quantidade de parcelas da despesa'
        ):
            criar_despesa(self.usuario, {
                'descricao': 'Notebook',
                'valor': '2000',
                'data': '2026-05-10',
                'categoria': self.categoria_despesa.id,
                'conta': 'Credito',
                'parcelada': 'on',
            })

    # Despesa nao pode usar categoria de receita.
    def test_despesa_nao_aceita_categoria_de_receita(self):

        with self.assertRaisesMessage(
            ValueError,
            'Categoria invalida'
        ):
            criar_despesa(self.usuario, {
                'descricao': 'Conta',
                'valor': '100',
                'data': '2026-05-10',
                'categoria': self.categoria_receita.id,
                'conta': 'Pix',
            })

    # Despesa valida deve ser criada e listada na competencia correta.
    def test_criar_e_listar_despesa_por_periodo(self):

        despesa = criar_despesa(self.usuario, {
            'descricao': 'Aluguel',
            'valor': '450',
            'data': '2026-05-10',
            'categoria': self.categoria_despesa.id,
            'conta': 'Debito',
        })

        despesas = listar_despesas_por_periodo(
            self.usuario,
            date(2026, 5, 1),
            date(2026, 5, 31)
        )

        self.assertIn(
            despesa,
            despesas
        )

    # Edicao deve permitir alterar dados principais da despesa.
    def test_editar_despesa_atualiza_dados(self):

        despesa = Despesa.objects.create(
            usuario=self.usuario,
            descricao='Antiga',
            valor=Decimal('100.00'),
            data=date(2026, 5, 1),
            categoria=self.categoria_despesa,
            conta='Pix'
        )

        atualizada = editar_despesa(despesa.id, self.usuario, {
            'descricao': 'Nova',
            'valor': '250',
            'data': '2026-05-15',
            'categoria': self.categoria_despesa.id,
            'conta': 'Debito',
        })

        self.assertEqual(
            atualizada.descricao,
            'Nova'
        )
        self.assertEqual(
            atualizada.conta,
            'Debito'
        )

    # Exclusao remove a despesa do banco.
    def test_excluir_despesa_remove_registro(self):

        despesa = Despesa.objects.create(
            usuario=self.usuario,
            descricao='Excluir',
            valor=Decimal('100.00'),
            data=date(2026, 5, 1),
            categoria=self.categoria_despesa,
            conta='Pix'
        )

        excluir_despesa(
            despesa.id,
            self.usuario
        )

        self.assertFalse(
            Despesa.objects.filter(id=despesa.id).exists()
        )
