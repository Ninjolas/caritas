from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bazar', '0002_categoriabazar_update_categorias'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='numero_operacao',
            field=models.CharField(blank=True, max_length=20, unique=True, null=True),
        ),
        migrations.AddField(
            model_name='venda',
            name='paroquia',
            field=models.CharField(blank=True, max_length=100, default=''),
        ),
        # After data is populated, remove null=True from numero_operacao
        migrations.AlterField(
            model_name='venda',
            name='numero_operacao',
            field=models.CharField(blank=True, max_length=20, unique=True, null=True),
        ),
    ]
