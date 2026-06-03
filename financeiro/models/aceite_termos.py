from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class AceiteTermos(models.Model):

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='aceite_termos'
    )

    aceitou = models.BooleanField(
        default=False
    )

    versao = models.CharField(
        max_length=20,
        default='2026-05-28'
    )

    aceito_em = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):

        return f"{self.usuario.username} - {self.versao}"
