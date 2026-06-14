import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('estoque', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BrechoEvento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('paroquia', models.CharField(max_length=100)),
                ('data', models.DateField()),
                ('descricao', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('planejado', 'Planejado'), ('em_andamento', 'Em andamento'), ('encerrado', 'Encerrado')], default='planejado', max_length=20)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('criado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='breches_criados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Evento de Brechó',
                'verbose_name_plural': 'Eventos de Brechó',
                'ordering': ['-data'],
            },
        ),
        migrations.CreateModel(
            name='VendaBrecho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(default=1)),
                ('preco_unitario', models.DecimalField(decimal_places=2, max_digits=8)),
                ('valor_total', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendas', to='brecho.brechoevento')),
                ('item_estoque', models.ForeignKey(limit_choices_to={'categoria': 'roupa'}, on_delete=django.db.models.deletion.PROTECT, related_name='vendas_brecho', to='estoque.itemestoque')),
                ('registrado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Venda do Brechó',
                'verbose_name_plural': 'Vendas do Brechó',
                'ordering': ['-criado_em'],
            },
        ),
    ]
