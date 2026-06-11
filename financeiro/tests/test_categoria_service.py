from decimal import Decimal

from financeiro.models import Despesa, Receita
from financeiro.services.categoria_service import (
    criar_categoria,
    editar_categoria,
    excluir_categoria,
    listar_categorias
)
from financeiro.models import Categoria
from financeiro.tests.base import FinanceiroTestCase


# Testa as regras de negocio ligadas as categorias.
class CategoriaServiceTestCase(FinanceiroTestCase):

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

    # Criacao valida nome, tipo e cor da categoria.
    def test_criar_categoria_valida_dados(self):

        categoria = criar_categoria(
            self.usuario,
            'Investimentos',
            Categoria.TIPO_RECEITA,
            '#62BFF0'
        )

        self.assertEqual(
            categoria.nome,
            'Investimentos'
        )
        self.assertEqual(
            categoria.tipo,
            Categoria.TIPO_RECEITA
        )

    # Categoria com tipo invalido deve ser recusada.
    def test_criar_categoria_recusa_tipo_invalido(self):

        with self.assertRaisesMessage(
            ValueError,
            'Tipo de categoria invalido'
        ):
            criar_categoria(
                self.usuario,
                'Teste',
                'outro',
                '#8FEBDD'
            )

    # Categoria com cor fora da paleta deve ser recusada.
    def test_criar_categoria_recusa_cor_invalida(self):

        with self.assertRaisesMessage(
            ValueError,
            'Cor de categoria invalida'
        ):
            criar_categoria(
                self.usuario,
                'Teste',
                Categoria.TIPO_DESPESA,
                '#FFFFFF'
            )

    # Edicao atualiza nome e cor da categoria.
    def test_editar_categoria_atualiza_nome_e_cor(self):

        categoria = editar_categoria(
            self.categoria_despesa.id,
            self.usuario,
            'Moradia',
            '#62BFF0'
        )

        self.assertEqual(
            categoria.nome,
            'Moradia'
        )
        self.assertEqual(
            categoria.cor,
            '#62BFF0'
        )

    # Exclusao de categoria remove lancamentos vinculados.
    def test_excluir_categoria_remove_lancamentos_vinculados(self):

        Receita.objects.create(
            usuario=self.usuario,
            descricao='Receita',
            valor=Decimal('100.00'),
            data='2026-05-10',
            categoria=self.categoria_receita
        )
        Despesa.objects.create(
            usuario=self.usuario,
            descricao='Despesa',
            valor=Decimal('50.00'),
            data='2026-05-10',
            categoria=self.categoria_receita,
            conta='Pix'
        )

        excluir_categoria(
            self.categoria_receita.id,
            self.usuario
        )

        self.assertFalse(
            Receita.objects.filter(categoria=self.categoria_receita).exists()
        )
        self.assertFalse(
            Despesa.objects.filter(categoria=self.categoria_receita).exists()
        )
