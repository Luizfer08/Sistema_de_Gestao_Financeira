from django.contrib.auth.models import User
from django.test import TestCase

from financeiro.models import Categoria


# Classe base com dados comuns usados pelos testes do app financeiro.
class FinanceiroTestCase(TestCase):

    def setUp(self):

        self.usuario = User.objects.create_user(
            username='teste',
            email='teste@email.com',
            password='123456'
        )

        self.outro_usuario = User.objects.create_user(
            username='outro',
            email='outro@email.com',
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

        self.categoria_receita_outro_usuario = Categoria.objects.create(
            usuario=self.outro_usuario,
            nome='Venda',
            tipo=Categoria.TIPO_RECEITA,
            cor='#62BFF0'
        )
