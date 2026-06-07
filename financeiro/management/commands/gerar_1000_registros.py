# BaseCommand permite criar comandos executados pelo manage.py.
from django.core.management.base import BaseCommand

# User localiza o perfil que recebera os registros.
from django.contrib.auth.models import User

# Models usados para criar categorias, receitas e despesas.
from financeiro.models import Receita, Despesa, Categoria

# Decimal mantem precisao nos valores financeiros.
from decimal import Decimal

# Funcoes usadas para gerar dados aleatorios.
from random import choice, randint, uniform

# Date e timedelta distribuem os lancamentos ao longo do ano.
from datetime import date, timedelta


# Comando usado para popular um usuario com dados de teste.
class Command(BaseCommand):

    # Texto exibido na ajuda do manage.py.
    help = "Gera 1000 registros aleatorios para o usuario teste1000"

    # Metodo executado quando o comando e chamado.
    def handle(self, *args, **kwargs):

        # Usuario criado para a demonstracao com grande volume de dados.
        usuario = User.objects.get(id=16)

        # Categorias de receita criadas automaticamente, se nao existirem.
        categorias_receita_nomes = [
            ("Salario", "#8FEBDD"),
            ("Freelance", "#62BFF0"),
            ("Investimentos", "#F5D7B8"),
            ("Vendas", "#99F69D"),
        ]

        # Categorias de despesa criadas automaticamente, se nao existirem.
        categorias_despesa_nomes = [
            ("Alimentacao", "#8FEBDD"),
            ("Moradia", "#5A4226"),
            ("Transporte", "#62BFF0"),
            ("Lazer", "#FEAB1B"),
            ("Educacao", "#594CF2"),
            ("Saude", "#FF073F"),
        ]

        categorias_receita = []

        # Get_or_create evita duplicar categorias a cada execucao.
        for nome, cor in categorias_receita_nomes:
            categoria, _ = Categoria.objects.get_or_create(
                usuario=usuario,
                nome=nome,
                tipo="receita",
                defaults={"cor": cor}
            )
            categorias_receita.append(categoria)

        categorias_despesa = []

        # Cria ou reaproveita categorias de despesas.
        for nome, cor in categorias_despesa_nomes:
            categoria, _ = Categoria.objects.get_or_create(
                usuario=usuario,
                nome=nome,
                tipo="despesa",
                defaults={"cor": cor}
            )
            categorias_despesa.append(categoria)

        # Descricoes usadas nas receitas falsas.
        descricoes_receita = [
            "Salario mensal",
            "Projeto freelance",
            "Venda online",
            "Rendimento investimento",
            "Bonus"
        ]

        # Descricoes usadas nas despesas falsas.
        descricoes_despesa = [
            "Mercado",
            "Aluguel",
            "Uber",
            "Internet",
            "Cinema",
            "Curso online",
            "Consulta medica"
        ]

        # Contas usadas somente nas despesas.
        contas = ["Pix", "Debito", "Credito", "Dinheiro"]

        # Gera 1000 registros misturando receitas e despesas.
        for i in range(1000):

            # Distribui as datas aleatoriamente no ultimo ano.
            data_aleatoria = date.today() - timedelta(days=randint(0, 365))

            # Gera valores monetarios entre 20 e 3000.
            valor = Decimal(str(round(uniform(20, 3000), 2)))

            # Parcela e fixa sao exclusivas para manter a regra do sistema.
            parcelada = choice([True, False, False])
            fixa = False if parcelada else choice([True, False, False])
            quantidade_parcelas = randint(2, 12) if parcelada else None

            # Sorteia se o registro sera receita ou despesa.
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
            self.style.SUCCESS(
                "1000 registros gerados com categorias, fixos e parcelados."
            )
        )
