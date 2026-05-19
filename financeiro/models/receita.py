# MODELS
from django.db import models

# USUÁRIO PADRÃO DO DJANGO
from django.contrib.auth.models import User

# MODEL DE CATEGORIAS
from .categoria import Categoria


# MODEL RESPONSÁVEL PELAS RECEITAS
class Receita(models.Model):

    # Usuário dono da receita
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receitas'
    )

    # Descrição da receita
    descricao = models.CharField(
        max_length=200
    )

    # Valor financeiro da receita
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Data da receita
    data = models.DateField()

    # Categoria vinculada à receita
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='receitas'
    )

    # Define se a receita é recorrente
    recorrente = models.BooleanField(
        default=False
    )

    # Define se a receita é parcelada
    parcelada = models.BooleanField(
        default=False
    )

    # Quantidade de parcelas
    quantidade_parcelas = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    # Data de criação do registro
    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    # Data final para receitas recorrentes
    data_fim = models.DateField(
        null=True,
        blank=True
    )

    # Representação textual da receita
    def __str__(self):

        return f"{self.descricao} - R$ {self.valor}"

    # Verifica se a receita está ativa em determinada data
    def is_ativa_em(self, data):

        """
        Verifica se a receita deve ser considerada
        em uma data específica
        """

        # RECEITA NÃO RECORRENTE
        # Só é válida na data exata
        if not self.recorrente:

            return self.data == data

        # RECEITA RECORRENTE AINDA NÃO INICIADA
        if data < self.data:

            return False

        # RECEITA RECORRENTE COM DATA FINAL
        if self.data_fim and data > self.data_fim:

            return False

        # RECEITA ATIVA
        return True