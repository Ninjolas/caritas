from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_usuario_paroquia_fk'),
        ('financeiro', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movimentacaofinanceira',
            name='paroquia',
        ),
        migrations.AddField(
            model_name='movimentacaofinanceira',
            name='paroquia',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='movimentacoes',
                to='accounts.paroquia',
                help_text='Preencher apenas se origem = Paróquia',
            ),
        ),
    ]
