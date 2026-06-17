import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bazar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaBazar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('ativa', models.BooleanField(default=True)),
                ('pai', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='subcategorias',
                    to='bazar.categoriabazar',
                )),
            ],
            options={
                'verbose_name': 'Categoria do Bazar',
                'verbose_name_plural': 'Categorias do Bazar',
                'ordering': ['pai__nome', 'nome'],
            },
        ),
        # ItemEstoqueBazar: drop old CharField, add FK
        migrations.RemoveField(model_name='itemestoquebazar', name='categoria'),
        migrations.AddField(
            model_name='itemestoquebazar',
            name='categoria',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='itens_estoque',
                to='bazar.categoriabazar',
            ),
        ),
        # ItemEntradaBazar: drop old CharField, add FK
        migrations.RemoveField(model_name='itementradabazar', name='categoria'),
        migrations.AddField(
            model_name='itementradabazar',
            name='categoria',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='itens_entrada',
                to='bazar.categoriabazar',
            ),
        ),
        # Update ordering meta
        migrations.AlterModelOptions(
            name='itemestoquebazar',
            options={
                'ordering': ['categoria__nome', 'tamanho'],
                'verbose_name': 'Item do Estoque do Bazar',
                'verbose_name_plural': 'Itens do Estoque do Bazar',
            },
        ),
    ]
