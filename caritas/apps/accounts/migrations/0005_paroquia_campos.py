from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_paroquia'),
    ]

    operations = [
        migrations.AddField(
            model_name='paroquia',
            name='cidade',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paroquia',
            name='bairro',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='paroquia',
            name='endereco',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='paroquia',
            name='telefone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='paroquia',
            name='email',
            field=models.EmailField(blank=True),
        ),
    ]
