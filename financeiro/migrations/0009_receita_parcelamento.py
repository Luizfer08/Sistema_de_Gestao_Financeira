# Generated manually for the new income form fields.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0008_despesa_conta_parcelamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='receita',
            name='parcelada',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='receita',
            name='quantidade_parcelas',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
