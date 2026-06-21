from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_usuario_paroquia_fk'),
        ('brecho', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brechoevento',
            name='paroquia',
        ),
        migrations.AddField(
            model_name='brechoevento',
            name='paroquia',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='eventos_brecho',
                to='accounts.paroquia',
            ),
        ),
    ]
