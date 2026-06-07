# Importa os recursos de modelagem do Django.
from django.db import models

# User representa o usuario autenticado dono dos registros.
from django.contrib.auth.models import User

# Categoria classifica a despesa dentro do controle financeiro.
from .categoria import Categoria


# Model responsavel por armazenar as despesas cadastradas pelo usuario.
class Despesa(models.Model):

    # Usuario dono da despesa. Ao excluir o usuario, suas despesas tambem saem.
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='despesas'
    )

    # Texto que identifica o motivo da despesa.
    descricao = models.CharField(
        max_length=255
    )

    # Valor monetario da despesa.
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Forma ou conta utilizada no pagamento.
    conta = models.CharField(
        max_length=50,
        blank=True,
        default=''
    )

    # Data inicial da despesa ou da primeira parcela.
    data = models.DateField()

    # Campo opcional para encerrar uma recorrencia futura, caso seja usado.
    data_fim = models.DateField(
        null=True,
        blank=True
    )

    # Indica uma despesa fixa, contabilizada nos meses seguintes.
    recorrente = models.BooleanField(
        default=False
    )

    # Indica uma despesa parcelada, limitada pela quantidade de parcelas.
    parcelada = models.BooleanField(
        default=False
    )

    # Quantidade de meses em que a despesa parcelada sera considerada.
    quantidade_parcelas = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    # Categoria da despesa. Despesas dependem da categoria cadastrada.
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='despesas'
    )

    # Data em que o registro foi criado no sistema.
    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    # Texto exibido no admin e em representacoes simples do objeto.
    def __str__(self):

        return f"{self.descricao} - R$ {self.valor}"

    # Verifica se a despesa deve entrar em uma data especifica.
    def is_ativa_em(self, data):

        # Despesa comum so aparece na propria data cadastrada.
        if not self.recorrente:

            return self.data == data

        # Despesa fixa ainda nao iniciada nao entra no calculo.
        if data < self.data:

            return False

        # Despesa fixa com data final deixa de entrar apos o encerramento.
        if self.data_fim and data > self.data_fim:

            return False

        # Despesa fixa ativa entra no calculo.
        return True
