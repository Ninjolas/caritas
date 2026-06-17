from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doacoes', '0002_itemdoacao_categoria_outro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doacao',
            name='tipo',
        ),
        migrations.AddField(
            model_name='itemdoacao',
            name='data_validade',
            field=models.DateField(blank=True, null=True),
        ),
    ]
