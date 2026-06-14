import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('estoque', '0001_initial'),
        ('familias', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CestaPronta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paroquia', models.CharField(max_length=100)),
                ('quantidade', models.IntegerField(default=0)),
                ('origem', models.CharField(choices=[('montagem', 'Montagem interna'), ('doacao', 'Doação recebida')], max_length=10)),
                ('data', models.DateField()),
                ('observacao', models.TextField(blank=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('registrado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cestas_registradas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Entrada de Cestas Prontas',
                'verbose_name_plural': 'Entradas de Cestas Prontas',
                'ordering': ['-data'],
            },
        ),
        migrations.CreateModel(
            name='ItemMontagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade_total', models.IntegerField(help_text='Quantidade total retirada do estoque para todas as cestas')),
                ('cesta_pronta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_usados', to='cestas.cestapronta')),
                ('item_estoque', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='usos_montagem', to='estoque.itemestoque')),
            ],
        ),
        migrations.CreateModel(
            name='EntregaCesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paroquia', models.CharField(max_length=100)),
                ('quantidade', models.IntegerField(default=1)),
                ('data', models.DateField()),
                ('observacao', models.TextField(blank=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('familia', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cestas_recebidas', to='familias.familia')),
                ('registrado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Entrega de Cesta',
                'verbose_name_plural': 'Entregas de Cestas',
                'ordering': ['-data'],
            },
        ),
    ]
