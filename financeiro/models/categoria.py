# MODELS
from django.db import models

# USUÁRIO PADRÃO DO DJANGO
from django.contrib.auth.models import User


# MODEL RESPONSÁVEL PELAS CATEGORIAS
class Categoria(models.Model):

    # TIPOS DE CATEGORIA
    TIPO_RECEITA = 'receita'
    TIPO_DESPESA = 'despesa'

    # OPÇÕES DISPONÍVEIS PARA O CAMPO TIPO
    TIPO_CHOICES = [
        (TIPO_RECEITA, 'Receita'),
        (TIPO_DESPESA, 'Despesa'),
    ]

    # Usuário dono da categoria
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    # Nome da categoria
    nome = models.CharField(
        max_length=100
    )

    # Tipo da categoria
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        default=TIPO_DESPESA
    )

    # Cor utilizada na interface e gráficos
    cor = models.CharField(
        max_length=7,
        default='#8FEBDD'
    )

    # Representação textual da categoria
    def __str__(self):

        return self.nome