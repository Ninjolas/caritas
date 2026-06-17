from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_usuario_perfil'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paroquia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150, unique=True)),
                ('ativa', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Paróquia',
                'verbose_name_plural': 'Paróquias',
                'ordering': ['nome'],
            },
        ),
    ]
