from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_usuario_paroquia_fk'),
        ('atendimentos', '0003_remove_doacao_alimentos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atendimento',
            name='paroquia',
        ),
        migrations.AddField(
            model_name='atendimento',
            name='paroquia',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='atendimentos',
                to='accounts.paroquia',
            ),
        ),
    ]
