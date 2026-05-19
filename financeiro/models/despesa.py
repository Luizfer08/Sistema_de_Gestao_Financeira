# MODELS
from django.db import models

# USUÁRIO PADRÃO DO DJANGO
from django.contrib.auth.models import User

# MODEL DE CATEGORIAS
from .categoria import Categoria


# MODEL RESPONSÁVEL PELAS DESPESAS
class Despesa(models.Model):

    # Usuário dono da despesa
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='despesas'
    )

    # Descrição da despesa
    descricao = models.CharField(
        max_length=255
    )

    # Valor financeiro da despesa
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Conta utilizada na despesa
    conta = models.CharField(
        max_length=50,
        blank=True,
        default=''
    )

    # Data principal da despesa
    data = models.DateField()

    # Data final para despesas recorrentes
    data_fim = models.DateField(
        null=True,
        blank=True
    )

    # Define se a despesa é recorrente
    recorrente = models.BooleanField(
        default=False
    )

    # Define se a despesa é parcelada
    parcelada = models.BooleanField(
        default=False
    )

    # Quantidade de parcelas
    quantidade_parcelas = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    # Categoria vinculada à despesa
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='despesas'
    )

    # Data de criação do registro
    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    # Representação textual da despesa
    def __str__(self):

        return f"{self.descricao} - R$ {self.valor}"

    # Verifica se a despesa está ativa em determinada data
    def is_ativa_em(self, data):

        """
        Verifica se a despesa deve ser considerada
        em uma data específica
        """

        # DESPESA NÃO RECORRENTE
        # Só é válida na data exata
        if not self.recorrente:

            return self.data == data

        # DESPESA RECORRENTE AINDA NÃO INICIADA
        if data < self.data:

            return False

        # DESPESA RECORRENTE COM DATA FINAL
        if self.data_fim and data > self.data_fim:

            return False

        # DESPESA ATIVA
        return True