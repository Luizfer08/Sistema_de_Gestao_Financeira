from django.db import models
from django.contrib.auth.models import User
from .categoria import Categoria


class Despesa(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='despesas'
    )

    descricao = models.CharField(max_length=255)

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    data = models.DateField()

    data_fim = models.DateField(null=True, blank=True)

    recorrente = models.BooleanField(default=False)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='despesas'
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"

    def is_ativa_em(self, data):
        """
        Verifica se a despesa deve ser considerada em uma data específica
        """

        # NÃO RECORRENTE → só no dia exato
        if not self.recorrente:
            return self.data == data

        # RECORRENTE → ainda não começou
        if data < self.data:
            return False

        # RECORRENTE COM FIM
        if self.data_fim and data > self.data_fim:
            return False

        return True