from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_usuario_paroquia_fk'),
        ('familias', '0002_familia_data_nascimento_familia_data_ultimo_atendimento_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='familia',
            name='paroquia_responsavel',
        ),
        migrations.AddField(
            model_name='familia',
            name='paroquia_responsavel',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='familias',
                to='accounts.paroquia',
            ),
        ),
    ]
