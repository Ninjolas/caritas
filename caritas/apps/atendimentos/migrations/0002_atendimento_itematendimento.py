import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atendimentos', '0001_initial'),
        ('estoque', '0002_itemestoque_categoria_outro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atendimento',
            name='tipo',
            field=models.CharField(
                choices=[
                    ('assistencia_social', 'Assistência Social'),
                    ('doacao_alimentos', 'Doação de Alimentos'),
                    ('doacao_roupas', 'Doação de Roupas'),
                    ('doacao_cesta_basica', 'Doação de Cesta Básica'),
                    ('encaminhamento', 'Encaminhamento'),
                    ('visita_domiciliar', 'Visita Domiciliar'),
                    ('outro', 'Outro'),
                ],
                max_length=30,
            ),
        ),
        migrations.CreateModel(
            name='ItemAtendimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_nome', models.CharField(max_length=200)),
                ('item_unidade', models.CharField(default='unidade', max_length=50)),
                ('quantidade', models.IntegerField()),
                ('atendimento', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='itens',
                    to='atendimentos.atendimento',
                )),
                ('item_estoque', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='usos_atendimento',
                    to='estoque.itemestoque',
                )),
            ],
        ),
    ]
