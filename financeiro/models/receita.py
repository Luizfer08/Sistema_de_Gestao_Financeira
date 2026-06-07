# Importa os recursos de modelagem do Django.
from django.db import models

# User representa o usuario autenticado dono dos registros.
from django.contrib.auth.models import User

# Categoria classifica a receita dentro do controle financeiro.
from .categoria import Categoria


# Model responsavel por armazenar as receitas cadastradas pelo usuario.
class Receita(models.Model):

    # Usuario dono da receita. Ao excluir o usuario, suas receitas tambem saem.
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receitas'
    )

    # Texto que identifica a origem da receita.
    descricao = models.CharField(
        max_length=200
    )

    # Valor monetario da receita.
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Data inicial da receita ou da primeira parcela.
    data = models.DateField()

    # Categoria da receita. Se a categoria for removida, a receita permanece.
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='receitas'
    )

    # Indica uma renda fixa, contabilizada nos meses seguintes.
    recorrente = models.BooleanField(
        default=False
    )

    # Indica uma receita parcelada, limitada pela quantidade de parcelas.
    parcelada = models.BooleanField(
        default=False
    )

    # Quantidade de meses em que a receita parcelada sera considerada.
    quantidade_parcelas = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    # Data em que o registro foi criado no sistema.
    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    # Campo opcional para encerrar uma recorrencia futura, caso seja usado.
    data_fim = models.DateField(
        null=True,
        blank=True
    )

    # Texto exibido no admin e em representacoes simples do objeto.
    def __str__(self):

        return f"{self.descricao} - R$ {self.valor}"

    # Verifica se a receita deve entrar em uma data especifica.
    def is_ativa_em(self, data):

        # Receita comum so aparece na propria data cadastrada.
        if not self.recorrente:

            return self.data == data

        # Receita fixa ainda nao iniciada nao entra no calculo.
        if data < self.data:

            return False

        # Receita fixa com data final deixa de entrar apos o encerramento.
        if self.data_fim and data > self.data_fim:

            return False

        # Receita fixa ativa entra no calculo.
        return True
