# Generated manually for the new expense form fields.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0007_categoria_tipo_cor'),
    ]

    operations = [
        migrations.AddField(
            model_name='despesa',
            name='conta',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='despesa',
            name='parcelada',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='despesa',
            name='quantidade_parcelas',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
