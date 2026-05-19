# Generated manually for category type and color support.

from django.db import migrations, models


def classificar_categorias_existentes(apps, schema_editor):
    Categoria = apps.get_model('financeiro', 'Categoria')
    Receita = apps.get_model('financeiro', 'Receita')
    Despesa = apps.get_model('financeiro', 'Despesa')

    for categoria in Categoria.objects.all():
        tem_receita = Receita.objects.filter(categoria_id=categoria.id).exists()
        tem_despesa = Despesa.objects.filter(categoria_id=categoria.id).exists()

        if tem_receita and not tem_despesa:
            categoria.tipo = 'receita'
            categoria.save(update_fields=['tipo'])


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0006_receita_data_fim'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='cor',
            field=models.CharField(default='#8FEBDD', max_length=7),
        ),
        migrations.AddField(
            model_name='categoria',
            name='tipo',
            field=models.CharField(
                choices=[('receita', 'Receita'), ('despesa', 'Despesa')],
                default='despesa',
                max_length=10,
            ),
        ),
        migrations.RunPython(
            classificar_categorias_existentes,
            migrations.RunPython.noop
        ),
    ]
