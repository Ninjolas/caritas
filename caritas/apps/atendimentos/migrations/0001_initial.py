import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('familias', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Atendimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('assistencia_social', 'Assistência Social'), ('doacao_alimentos', 'Doação de Alimentos'), ('doacao_roupas', 'Doação de Roupas'), ('encaminhamento', 'Encaminhamento'), ('visita_domiciliar', 'Visita Domiciliar'), ('outro', 'Outro')], max_length=30)),
                ('data', models.DateField()),
                ('descricao', models.TextField()),
                ('paroquia', models.CharField(max_length=100)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('familia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atendimentos', to='familias.familia')),
                ('registrado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Atendimento',
                'verbose_name_plural': 'Atendimentos',
                'ordering': ['-data'],
            },
        ),
    ]
