from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0010_receita_conta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receita',
            name='conta',
        ),
    ]
