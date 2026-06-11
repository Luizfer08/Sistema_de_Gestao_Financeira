from datetime import date
from decimal import Decimal

from financeiro.models import Receita
from financeiro.services.receita_service import (
    criar_receita,
    editar_receita,
    excluir_receita,
    listar_receitas_por_periodo
)
from financeiro.tests.base import FinanceiroTestCase


# Testa as regras de negocio ligadas ao cadastro de receitas.
class ReceitaServiceTestCase(FinanceiroTestCase):

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

    # Receita parcelada precisa informar quantidade de parcelas.
    def test_receita_parcelada_exige_quantidade_de_parcelas(self):

        with self.assertRaisesMessage(
            ValueError,
            'Informe a quantidade de parcelas da receita'
        ):
            criar_receita(self.usuario, {
                'descricao': 'Projeto',
                'valor': '1200',
                'data': '2026-05-10',
                'categoria': self.categoria_receita.id,
                'parcelada': 'on',
            })

    # Receita nao pode usar categoria de outro usuario.
    def test_receita_nao_aceita_categoria_de_outro_usuario(self):

        with self.assertRaisesMessage(
            ValueError,
            'Categoria invalida'
        ):
            criar_receita(self.usuario, {
                'descricao': 'Venda',
                'valor': '800',
                'data': '2026-05-10',
                'categoria': self.categoria_receita_outro_usuario.id,
            })

    # Receita valida deve ser criada e listada na competencia correta.
    def test_criar_e_listar_receita_por_periodo(self):

        receita = criar_receita(self.usuario, {
            'descricao': 'Trabalho',
            'valor': '1000',
            'data': '2026-05-10',
            'categoria': self.categoria_receita.id,
        })

        receitas = listar_receitas_por_periodo(
            self.usuario,
            date(2026, 5, 1),
            date(2026, 5, 31)
        )

        self.assertIn(
            receita,
            receitas
        )

    # Edicao deve permitir alterar dados principais da receita.
    def test_editar_receita_atualiza_dados(self):

        receita = Receita.objects.create(
            usuario=self.usuario,
            descricao='Antiga',
            valor=Decimal('100.00'),
            data=date(2026, 5, 1),
            categoria=self.categoria_receita
        )

        atualizada = editar_receita(receita.id, self.usuario, {
            'descricao': 'Nova',
            'valor': '250',
            'data': '2026-05-15',
            'categoria': self.categoria_receita.id,
        })

        self.assertEqual(
            atualizada.descricao,
            'Nova'
        )
        self.assertEqual(
            atualizada.valor,
            Decimal('250')
        )

    # Exclusao remove a receita do banco.
    def test_excluir_receita_remove_registro(self):

        receita = Receita.objects.create(
            usuario=self.usuario,
            descricao='Excluir',
            valor=Decimal('100.00'),
            data=date(2026, 5, 1),
            categoria=self.categoria_receita
        )

        excluir_receita(
            receita.id,
            self.usuario
        )

        self.assertFalse(
            Receita.objects.filter(id=receita.id).exists()
        )
