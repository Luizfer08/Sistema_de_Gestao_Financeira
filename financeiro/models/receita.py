from django.db import models
from django.contrib.auth.models import User
from .categoria import Categoria

class Receita(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    recorrente = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao