from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0004_itemestoque_paroquia_fk'),
        ('accounts', '0006_usuario_paroquia_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='produtocatalogo',
            name='paroquia',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='catalogo_produtos',
                to='accounts.paroquia',
            ),
        ),
        migrations.AlterUniqueTogether(
            name='produtocatalogo',
            unique_together={('nome', 'paroquia')},
        ),
        migrations.AlterField(
            model_name='produtocatalogo',
            name='nome',
            field=models.CharField(max_length=200),
        ),
    ]
