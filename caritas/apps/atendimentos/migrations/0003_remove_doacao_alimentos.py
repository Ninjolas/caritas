from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atendimentos', '0002_atendimento_itematendimento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atendimento',
            name='tipo',
            field=models.CharField(
                choices=[
                    ('assistencia_social', 'Assistência Social'),
                    ('doacao_roupas', 'Doação de Roupas'),
                    ('doacao_cesta_basica', 'Doação de Cesta Básica'),
                    ('encaminhamento', 'Encaminhamento'),
                    ('visita_domiciliar', 'Visita Domiciliar'),
                    ('outro', 'Outro'),
                ],
                max_length=30,
            ),
        ),
    ]
