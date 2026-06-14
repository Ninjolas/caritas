from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('familias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='familia',
            name='nome_mae',
            field=models.CharField(default='', max_length=200, verbose_name='Nome da mãe'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='familia',
            name='nome_pai',
            field=models.CharField(blank=True, max_length=200, verbose_name='Nome do pai'),
        ),
        migrations.AddField(
            model_name='familia',
            name='data_nascimento',
            field=models.DateField(blank=True, null=True, verbose_name='Data de nascimento'),
        ),
        migrations.AddField(
            model_name='familia',
            name='data_ultima_visita',
            field=models.DateField(blank=True, null=True, verbose_name='Data da última visita domiciliar'),
        ),
        migrations.AddField(
            model_name='familia',
            name='data_ultimo_atendimento',
            field=models.DateField(blank=True, null=True, verbose_name='Data do último atendimento'),
        ),
        migrations.AlterModelOptions(
            name='familia',
            options={'ordering': ['responsavel_nome'], 'verbose_name': 'Família', 'verbose_name_plural': 'Famílias'},
        ),
    ]
