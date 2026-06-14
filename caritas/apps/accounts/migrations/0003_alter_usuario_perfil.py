from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_usuario_groups_alter_usuario_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='perfil',
            field=models.CharField(
                choices=[
                    ('voluntario', 'Voluntário'),
                    ('coordenador', 'Coordenador'),
                    ('administrador', 'Administrador'),
                    ('coordenador_bazar', 'Coordenador do Bazar'),
                    ('voluntario_bazar', 'Voluntário do Bazar'),
                ],
                default='voluntario',
                max_length=20,
            ),
        ),
    ]
