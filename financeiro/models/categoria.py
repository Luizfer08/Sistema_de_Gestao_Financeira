# Importa os recursos de modelagem do Django.
from django.db import models

# User representa o usuario autenticado dono das categorias.
from django.contrib.auth.models import User


# Model responsavel por separar receitas e despesas por categoria.
class Categoria(models.Model):

    # Tipos internos usados para diferenciar receitas e despesas.
    TIPO_RECEITA = 'receita'
    TIPO_DESPESA = 'despesa'

    # Opcoes exibidas e validadas pelo Django para o campo tipo.
    TIPO_CHOICES = [
        (TIPO_RECEITA, 'Receita'),
        (TIPO_DESPESA, 'Despesa'),
    ]

    # Usuario dono da categoria.
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    # Nome exibido nas telas, tabelas e graficos.
    nome = models.CharField(
        max_length=100
    )

    # Define se a categoria pertence a receitas ou despesas.
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        default=TIPO_DESPESA
    )

    # Cor usada no ponto da tabela e no grafico de categorias.
    cor = models.CharField(
        max_length=7,
        default='#8FEBDD'
    )

    # Texto exibido no admin e em selects do sistema.
    def __str__(self):

        return self.nome
