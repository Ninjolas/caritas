import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmpresaParceira',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('cnpj', models.CharField(blank=True, max_length=18)),
                ('contato_nome', models.CharField(blank=True, max_length=200)),
                ('contato_telefone', models.CharField(blank=True, max_length=20)),
                ('contato_email', models.EmailField(blank=True)),
                ('ativa', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Empresa Parceira',
                'verbose_name_plural': 'Empresas Parceiras',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='ItemEstoqueBazar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=200)),
                ('categoria', models.CharField(choices=[('masculino_adulto', 'Masculino Adulto'), ('feminino_adulto', 'Feminino Adulto'), ('infantil', 'Infantil'), ('calcados', 'Calçados'), ('acessorios', 'Acessórios'), ('outro', 'Outro')], max_length=20)),
                ('tamanho', models.CharField(choices=[('pp', 'PP'), ('p', 'P'), ('m', 'M'), ('g', 'G'), ('gg', 'GG'), ('xgg', 'XGG'), ('unico', 'Único')], default='unico', max_length=10)),
                ('estado', models.CharField(choices=[('novo', 'Novo'), ('bom', 'Bom estado'), ('regular', 'Regular')], default='bom', max_length=10)),
                ('quantidade', models.IntegerField(default=0)),
                ('preco_sugerido', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('registrado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Item do Estoque do Bazar',
                'verbose_name_plural': 'Itens do Estoque do Bazar',
                'ordering': ['categoria', 'tamanho'],
            },
        ),
        migrations.CreateModel(
            name='EntradaBazar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_entrada', models.CharField(choices=[('doacao_item', 'Doação de itens'), ('doacao_financeira', 'Doação financeira')], max_length=20)),
                ('tipo_doador', models.CharField(choices=[('pessoa_fisica', 'Pessoa Física'), ('empresa', 'Empresa Parceira')], max_length=20)),
                ('doador_nome', models.CharField(blank=True, max_length=200)),
                ('doador_contato', models.CharField(blank=True, max_length=100)),
                ('valor', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('data', models.DateField()),
                ('observacao', models.TextField(blank=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bazar.empresaparceira')),
                ('registrado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entradas_bazar', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Entrada do Bazar',
                'verbose_name_plural': 'Entradas do Bazar',
                'ordering': ['-data'],
            },
        ),
        migrations.CreateModel(
            name='ItemEntradaBazar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=200)),
                ('categoria', models.CharField(choices=[('masculino_adulto', 'Masculino Adulto'), ('feminino_adulto', 'Feminino Adulto'), ('infantil', 'Infantil'), ('calcados', 'Calçados'), ('acessorios', 'Acessórios'), ('outro', 'Outro')], max_length=20)),
                ('tamanho', models.CharField(choices=[('pp', 'PP'), ('p', 'P'), ('m', 'M'), ('g', 'G'), ('gg', 'GG'), ('xgg', 'XGG'), ('unico', 'Único')], default='unico', max_length=10)),
                ('estado', models.CharField(choices=[('novo', 'Novo'), ('bom', 'Bom estado'), ('regular', 'Regular')], default='bom', max_length=10)),
                ('quantidade', models.IntegerField(default=1)),
                ('preco_sugerido', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('entrada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='bazar.entradabazar')),
            ],
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(default=1)),
                ('preco_unitario', models.DecimalField(decimal_places=2, max_digits=8)),
                ('valor_total', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('data', models.DateField()),
                ('observacao', models.TextField(blank=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vendas', to='bazar.itemestoquebazar')),
                ('registrado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Venda',
                'verbose_name_plural': 'Vendas',
                'ordering': ['-data'],
            },
        ),
    ]
