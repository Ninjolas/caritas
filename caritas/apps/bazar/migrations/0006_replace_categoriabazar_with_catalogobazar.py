from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bazar', '0005_descricao_blank'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogoBazar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='Tipo de roupa')),
                ('genero', models.CharField(
                    choices=[
                        ('masculino', 'Masculino'),
                        ('feminino', 'Feminino'),
                        ('infantil', 'Infantil'),
                        ('unissex', 'Unissex'),
                    ],
                    max_length=20, verbose_name='Gênero'
                )),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Item do Catálogo',
                'verbose_name_plural': 'Catálogo do Bazar',
                'ordering': ['nome', 'genero'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='catalogobazar',
            unique_together={('nome', 'genero')},
        ),
        migrations.AddField(
            model_name='itemestoquebazar',
            name='catalogo',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='itens_estoque',
                to='bazar.catalogobazar',
                verbose_name='Catálogo',
            ),
        ),
        migrations.AddField(
            model_name='itementradabazar',
            name='catalogo',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='itens_entrada',
                to='bazar.catalogobazar',
                verbose_name='Catálogo',
            ),
        ),
        migrations.RemoveField(
            model_name='itemestoquebazar',
            name='categoria',
        ),
        migrations.RemoveField(
            model_name='itementradabazar',
            name='categoria',
        ),
        migrations.DeleteModel(
            name='CategoriaBazar',
        ),
    ]
