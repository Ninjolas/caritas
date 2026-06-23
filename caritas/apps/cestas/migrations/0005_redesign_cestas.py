import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cestas', '0004_entregacesta_familia_cascade'),
        ('estoque', '0007_produtocatalogo_categoria_outro'),
        ('familias', '0004_familia_id_interno_null_nome_pai_required'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Remove old models (children first)
        migrations.DeleteModel(name='ItemMontagem'),
        migrations.DeleteModel(name='EntregaCesta'),
        migrations.DeleteModel(name='CestaPronta'),

        # ModeloCesta
        migrations.CreateModel(
            name='ModeloCesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('paroquia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modelos_cesta', to='accounts.paroquia')),
            ],
            options={'verbose_name': 'Modelo de Cesta', 'verbose_name_plural': 'Modelos de Cesta', 'ordering': ['nome']},
        ),
        migrations.CreateModel(
            name='ModeloItemCesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('quantidade', models.IntegerField(default=1)),
                ('unidade', models.CharField(default='unidade', max_length=50)),
                ('modelo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='cestas.modelocesta')),
            ],
        ),

        # CestaRecebida
        migrations.CreateModel(
            name='CestaRecebida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('doador_nome', models.CharField(blank=True, max_length=200, verbose_name='Doador')),
                ('observacao', models.TextField(blank=True, verbose_name='Observacao')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('paroquia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cestas_recebidas', to='accounts.paroquia')),
                ('registrado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': 'Cesta Recebida', 'verbose_name_plural': 'Cestas Recebidas', 'ordering': ['-data']},
        ),
        migrations.CreateModel(
            name='ItemCestaRecebida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('quantidade', models.IntegerField()),
                ('unidade', models.CharField(default='unidade', max_length=50)),
                ('validade', models.DateField(blank=True, null=True)),
                ('cesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='cestas.cestarecebida')),
                ('produto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='estoque.produtocatalogo')),
            ],
        ),

        # CestaEntregue
        migrations.CreateModel(
            name='CestaEntregue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('observacao', models.TextField(blank=True, verbose_name='Observacao')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('familia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cestas_entregues', to='familias.familia')),
                ('modelo_usado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cestas.modelocesta', verbose_name='Modelo de cesta')),
                ('paroquia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cestas_entregues', to='accounts.paroquia')),
                ('registrado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': 'Cesta Entregue', 'verbose_name_plural': 'Cestas Entregues', 'ordering': ['-data']},
        ),
        migrations.CreateModel(
            name='ItemCestaEntregue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_nome', models.CharField(max_length=200)),
                ('item_unidade', models.CharField(default='unidade', max_length=50)),
                ('quantidade', models.IntegerField()),
                ('cesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='cestas.cestaentregue')),
                ('item_estoque', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usos_cesta', to='estoque.itemestoque')),
            ],
        ),
    ]
