from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0006_produtocatalogo_roupa_calcado'),
    ]

    operations = [
        migrations.AddField(
            model_name='produtocatalogo',
            name='categoria_outro',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Descrição (outro)'),
        ),
    ]
