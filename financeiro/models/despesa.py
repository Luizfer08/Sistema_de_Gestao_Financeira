from django.db import models
from django.contrib.auth.models import User
from .categoria import Categoria


class Despesa(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    descricao = models.CharField(max_length=255)

    valor = models.DecimalField(max_digits=10, decimal_places=2)

    data = models.DateField()

    data_fim = models.DateField(null=True, blank=True)

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    recorrente = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao