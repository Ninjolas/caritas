from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_usuario_paroquia_fk'),
        ('bazar', '0003_venda_campos_comprovante'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venda',
            name='paroquia',
        ),
        migrations.AddField(
            model_name='venda',
            name='paroquia',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='vendas_bazar',
                to='accounts.paroquia',
            ),
        ),
    ]
