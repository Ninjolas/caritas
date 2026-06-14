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
            name='MovimentacaoFinanceira',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origem', models.CharField(choices=[('diocese', 'Diocese'), ('paroquia', 'Paróquia')], max_length=10)),
                ('paroquia', models.CharField(blank=True, help_text='Preencher apenas se origem = Paróquia', max_length=100)),
                ('tipo', models.CharField(choices=[('entrada_doacao', 'Entrada — Doação espontânea'), ('entrada_vendas', 'Entrada — Receita de vendas'), ('saida_insumos', 'Saída — Compra de insumos'), ('saida_projeto', 'Saída — Aquisição para projeto'), ('saida_doacao_terceiros', 'Saída — Doação a projeto de terceiros')], max_length=30)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=12)),
                ('data', models.DateField()),
                ('descricao', models.TextField()),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('registrado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Movimentação Financeira',
                'verbose_name_plural': 'Movimentações Financeiras',
                'ordering': ['-data'],
            },
        ),
    ]
