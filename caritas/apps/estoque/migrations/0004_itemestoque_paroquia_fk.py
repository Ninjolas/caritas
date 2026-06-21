from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_usuario_paroquia_fk'),
        ('estoque', '0003_produtocatalogo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemestoque',
            name='paroquia',
        ),
        migrations.AddField(
            model_name='itemestoque',
            name='paroquia',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='itens_estoque',
                to='accounts.paroquia',
            ),
        ),
    ]
