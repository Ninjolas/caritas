from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_paroquia_campos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='paroquia',
        ),
        migrations.AddField(
            model_name='usuario',
            name='paroquia',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='usuarios',
                to='accounts.paroquia',
            ),
        ),
    ]
