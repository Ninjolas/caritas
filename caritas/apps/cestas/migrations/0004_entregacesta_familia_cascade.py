from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cestas', '0003_itemmontagem_set_null'),
        ('familias', '0003_familia_paroquia_fk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entregacesta',
            name='familia',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='cestas_recebidas',
                to='familias.familia',
            ),
        ),
    ]
