import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Familia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_interno', models.CharField(blank=True, max_length=50, unique=True)),
                ('possui_cpf', models.BooleanField(default=True)),
                ('cpf', models.CharField(blank=True, max_length=14, null=True)),
                ('responsavel_nome', models.CharField(max_length=200)),
                ('nacionalidade', models.CharField(max_length=100)),
                ('endereco', models.CharField(max_length=300)),
                ('telefone', models.CharField(blank=True, max_length=20)),
                ('escolaridade', models.CharField(
                    choices=[
                        ('fundamental_incompleto', 'Fundamental Incompleto'),
                        ('fundamental_completo', 'Fundamental Completo'),
                        ('medio_incompleto', 'Médio Incompleto'),
                        ('medio_completo', 'Médio Completo'),
                        ('superior', 'Superior'),
                    ],
                    max_length=30,
                )),
                ('ocupacao', models.CharField(blank=True, max_length=100)),
                ('local_trabalho', models.CharField(blank=True, max_length=200)),
                ('situacao_vulnerabilidade', models.TextField(blank=True)),
                ('renda_familiar', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bolsa_familia', models.BooleanField(default=False)),
                ('valor_beneficio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('qtd_pessoas', models.IntegerField()),
                ('qtd_criancas', models.IntegerField(default=0)),
                ('paroquia_responsavel', models.CharField(max_length=100)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('criado_por', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='familias_cadastradas',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'verbose_name': 'Família',
                'verbose_name_plural': 'Famílias',
                'ordering': ['-criado_em'],
            },
        ),
        migrations.CreateModel(
            name='Dependente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('idade', models.IntegerField()),
                ('genero', models.CharField(
                    choices=[('masculino', 'Masculino'), ('feminino', 'Feminino'), ('outro', 'Outro')],
                    max_length=20,
                )),
                ('familia', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='dependentes',
                    to='familias.familia',
                )),
            ],
            options={
                'verbose_name': 'Dependente',
                'verbose_name_plural': 'Dependentes',
            },
        ),
    ]
