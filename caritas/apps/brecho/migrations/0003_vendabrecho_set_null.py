from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0004_itemestoque_paroquia_fk'),
        ('brecho', '0002_brechoevento_paroquia_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendabrecho',
            name='item_nome',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='vendabrecho',
            name='item_estoque',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='vendas_brecho',
                to='estoque.itemestoque',
                limit_choices_to={'categoria': 'roupa'},
            ),
        ),
    ]
