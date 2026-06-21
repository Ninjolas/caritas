from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_usuario_paroquia_fk'),
        ('doacoes', '0003_doacao_remove_tipo_itemdoacao_data_validade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doacao',
            name='paroquia',
        ),
        migrations.AddField(
            model_name='doacao',
            name='paroquia',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='doacoes',
                to='accounts.paroquia',
            ),
        ),
    ]
