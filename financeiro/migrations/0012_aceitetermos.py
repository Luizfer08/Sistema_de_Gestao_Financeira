import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0011_remove_receita_conta'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AceiteTermos',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                ('aceitou', models.BooleanField(default=False)),
                ('versao', models.CharField(default='2026-05-28', max_length=20)),
                ('aceito_em', models.DateTimeField(default=django.utils.timezone.now)),
                (
                    'usuario',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='aceite_termos',
                        to=settings.AUTH_USER_MODEL
                    )
                ),
            ],
        ),
    ]
