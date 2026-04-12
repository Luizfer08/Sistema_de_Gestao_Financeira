from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from financeiro.models import Receita, Despesa, Categoria
import random
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Popula o banco com dados fictícios'

    def handle(self, *args, **kwargs):

        # ===== USUÁRIO =====
        user, _ = User.objects.get_or_create(
            username='teste',
            defaults={'email': 'teste@email.com'}
        )
        user.set_password('123456')
        user.save()

        # ===== CATEGORIAS =====
        nomes_categorias = [
            'Alimentação', 'Transporte', 'Moradia',
            'Lazer', 'Saúde', 'Educação',
            'Investimentos', 'Salário', 'Freelance'
        ]

        categorias = []
        for nome in nomes_categorias:
            cat, _ = Categoria.objects.get_or_create(
                nome=nome,
                usuario=user
            )
            categorias.append(cat)
        # ===== FUNÇÃO DATA ALEATÓRIA =====
        def data_aleatoria():
            hoje = date.today()
            dias = random.randint(0, 365)
            return hoje - timedelta(days=dias)

        # ===== RECEITAS =====
        for _ in range(1000):
            Receita.objects.create(
                usuario=user,
                descricao=f"Receita {_}",
                valor=random.uniform(50, 5000),
                data=data_aleatoria(),
                categoria=random.choice(categorias),
                recorrente=random.choice([True, False])
            )

        # ===== DESPESAS =====
        for _ in range(1000):
            Despesa.objects.create(
                usuario=user,
                descricao=f"Despesa {_}",
                valor=random.uniform(20, 3000),
                data=data_aleatoria(),
                categoria=random.choice(categorias),
                recorrente=random.choice([True, False])
            )

        self.stdout.write(self.style.SUCCESS('Dados populados com sucesso!'))