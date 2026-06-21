import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0002_itemestoque_categoria_outro'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProdutoCatalogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, unique=True)),
                ('categoria', models.CharField(choices=[('alimento', 'Alimento'), ('roupa', 'Roupa'), ('medicamento', 'Medicamento'), ('outro', 'Outro')], max_length=20)),
                ('unidade_padrao', models.CharField(default='unidade', max_length=50)),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Catálogo de Produtos',
                'ordering': ['categoria', 'nome'],
            },
        ),
        migrations.AddField(
            model_name='itemestoque',
            name='produto',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='itens_estoque',
                to='estoque.produtocatalogo',
            ),
        ),
    ]
