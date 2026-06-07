# User vincula o aceite aos dados de login do usuario.
from django.contrib.auth.models import User

# Models cria a estrutura da tabela no banco de dados.
from django.db import models

# Timezone registra a data e hora do aceite conforme configuracao do Django.
from django.utils import timezone


# Model que registra o aceite dos termos de uso e politica de privacidade.
class AceiteTermos(models.Model):

    # Cada usuario possui apenas um registro de aceite.
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='aceite_termos'
    )

    # Informa se o usuario aceitou os termos.
    aceitou = models.BooleanField(
        default=False
    )

    # Guarda a versao do texto aceito pelo usuario.
    versao = models.CharField(
        max_length=20,
        default='2026-05-28'
    )

    # Data e hora em que o aceite foi registrado.
    aceito_em = models.DateTimeField(
        default=timezone.now
    )

    # Texto exibido no admin do Django.
    def __str__(self):

        return f"{self.usuario.username} - {self.versao}"
