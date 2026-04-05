from django.db import models
from django.contrib.auth.models import User
from .categoria import Categoria


class Receita(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receitas'
    )

    descricao = models.CharField(max_length=200)

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    data = models.DateField()

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='receitas'
    )

    recorrente = models.BooleanField(default=False)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"

    def is_ativa_em(self, data):
        """
        Verifica se a receita deve ser considerada até uma data
        """
        return self.data <= data