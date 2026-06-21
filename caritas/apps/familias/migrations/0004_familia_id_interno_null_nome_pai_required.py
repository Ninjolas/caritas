from django.db import migrations, models


def convert_empty_id_interno_to_null(apps, schema_editor):
    Familia = apps.get_model('familias', 'Familia')
    Familia.objects.filter(id_interno='').update(id_interno=None)


class Migration(migrations.Migration):

    dependencies = [
        ('familias', '0003_familia_paroquia_fk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familia',
            name='id_interno',
            field=models.CharField(blank=True, default=None, max_length=50, null=True, unique=True),
        ),
        migrations.RunPython(convert_empty_id_interno_to_null, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='familia',
            name='nome_pai',
            field=models.CharField(max_length=200, verbose_name='Nome do pai'),
        ),
    ]
