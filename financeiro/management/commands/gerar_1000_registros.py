from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from financeiro.models import Receita, Despesa, Categoria
from decimal import Decimal
from random import choice, randint, uniform
from datetime import date, timedelta


class Command(BaseCommand):
    help = "Gera 1000 registros aleatórios para o usuário teste1000"

    def handle(self, *args, **kwargs):
        usuario = User.objects.get(id=16)

        categorias_receita_nomes = [
            ("Salário", "#8FEBDD"),
            ("Freelance", "#62BFF0"),
            ("Investimentos", "#F5D7B8"),
            ("Vendas", "#99F69D"),
        ]

        categorias_despesa_nomes = [
            ("Alimentação", "#8FEBDD"),
            ("Moradia", "#5A4226"),
            ("Transporte", "#62BFF0"),
            ("Lazer", "#FEAB1B"),
            ("Educação", "#594CF2"),
            ("Saúde", "#FF073F"),
        ]

        categorias_receita = []
        for nome, cor in categorias_receita_nomes:
            categoria, _ = Categoria.objects.get_or_create(
                usuario=usuario,
                nome=nome,
                tipo="receita",
                defaults={"cor": cor}
            )
            categorias_receita.append(categoria)

        categorias_despesa = []
        for nome, cor in categorias_despesa_nomes:
            categoria, _ = Categoria.objects.get_or_create(
                usuario=usuario,
                nome=nome,
                tipo="despesa",
                defaults={"cor": cor}
            )
            categorias_despesa.append(categoria)

        descricoes_receita = [
            "Salário mensal",
            "Projeto freelance",
            "Venda online",
            "Rendimento investimento",
            "Bônus"
        ]

        descricoes_despesa = [
            "Mercado",
            "Aluguel",
            "Uber",
            "Internet",
            "Cinema",
            "Curso online",
            "Consulta médica"
        ]

        contas = ["Pix", "Débito", "Crédito", "Dinheiro"]

        for i in range(1000):
            data_aleatoria = date.today() - timedelta(days=randint(0, 365))
            valor = Decimal(str(round(uniform(20, 3000), 2)))

            parcelada = choice([True, False, False])
            fixa = False if parcelada else choice([True, False, False])
            quantidade_parcelas = randint(2, 12) if parcelada else None

            if randint(0, 1) == 0:
                Receita.objects.create(
                    usuario=usuario,
                    descricao=choice(descricoes_receita),
                    valor=valor,
                    data=data_aleatoria,
                    categoria=choice(categorias_receita),
                    recorrente=fixa,
                    parcelada=parcelada,
                    quantidade_parcelas=quantidade_parcelas
                )
            else:
                Despesa.objects.create(
                    usuario=usuario,
                    descricao=choice(descricoes_despesa),
                    valor=valor,
                    data=data_aleatoria,
                    categoria=choice(categorias_despesa),
                    conta=choice(contas),
                    recorrente=fixa,
                    parcelada=parcelada,
                    quantidade_parcelas=quantidade_parcelas
                )

        self.stdout.write(
            self.style.SUCCESS("1000 registros gerados com categorias, fixos e parcelados.")
        )