from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_usuario_paroquia_fk'),
        ('atendimentos', '0004_atendimento_paroquia_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='atendimento',
            name='tipo_outro',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Especifique'),
        ),
        migrations.AddField(
            model_name='atendimento',
            name='paroquia_destino',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='encaminhamentos_recebidos',
                to='accounts.paroquia',
                verbose_name='Paróquia de destino',
            ),
        ),
    ]
