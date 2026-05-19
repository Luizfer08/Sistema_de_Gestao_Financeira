# Generated manually for income account support.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0009_receita_parcelamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='receita',
            name='conta',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
    
