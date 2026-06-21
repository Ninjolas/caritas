from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bazar', '0004_venda_paroquia_fk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemestoquebazar',
            name='descricao',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='itementradabazar',
            name='descricao',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
