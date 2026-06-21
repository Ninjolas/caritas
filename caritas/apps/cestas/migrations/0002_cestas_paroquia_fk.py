from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_usuario_paroquia_fk'),
        ('cestas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cestapronta',
            name='paroquia',
        ),
        migrations.AddField(
            model_name='cestapronta',
            name='paroquia',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='cestas_prontas',
                to='accounts.paroquia',
            ),
        ),
        migrations.RemoveField(
            model_name='entregacesta',
            name='paroquia',
        ),
        migrations.AddField(
            model_name='entregacesta',
            name='paroquia',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='entregas_cesta',
                to='accounts.paroquia',
            ),
        ),
    ]
