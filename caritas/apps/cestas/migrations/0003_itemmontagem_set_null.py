from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0004_itemestoque_paroquia_fk'),
        ('cestas', '0002_cestas_paroquia_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemmontagem',
            name='item_nome',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='itemmontagem',
            name='item_estoque',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='usos_montagem',
                to='estoque.itemestoque',
            ),
        ),
    ]
