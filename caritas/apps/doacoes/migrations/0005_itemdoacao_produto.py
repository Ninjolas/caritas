from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0004_itemestoque_paroquia_fk'),
        ('doacoes', '0004_doacao_paroquia_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemdoacao',
            name='produto',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='itens_doacao',
                to='estoque.produtocatalogo',
            ),
        ),
        migrations.AlterField(
            model_name='itemdoacao',
            name='nome',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='itemdoacao',
            name='categoria',
            field=models.CharField(
                blank=True, max_length=20,
                choices=[('alimento', 'Alimento'), ('roupa', 'Roupa'), ('medicamento', 'Medicamento'), ('outro', 'Outro')],
            ),
        ),
        migrations.RemoveField(
            model_name='itemdoacao',
            name='categoria_outro',
        ),
    ]
