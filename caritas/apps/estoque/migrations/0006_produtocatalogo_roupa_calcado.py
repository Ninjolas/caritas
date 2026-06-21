from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0005_produtocatalogo_paroquia'),
    ]

    operations = [
        migrations.AddField(
            model_name='produtocatalogo',
            name='genero',
            field=models.CharField(
                blank=True, max_length=20,
                choices=[('masculino', 'Masculino'), ('feminino', 'Feminino'), ('infantil', 'Infantil'), ('unissex', 'Unissex')],
            ),
        ),
        migrations.AddField(
            model_name='produtocatalogo',
            name='tamanho',
            field=models.CharField(
                blank=True, max_length=10,
                choices=[('pp', 'PP'), ('p', 'P'), ('m', 'M'), ('g', 'G'), ('gg', 'GG'), ('xgg', 'XGG'), ('unico', 'Único')],
            ),
        ),
        migrations.AddField(
            model_name='produtocatalogo',
            name='tipo_calcado',
            field=models.CharField(
                blank=True, max_length=20,
                choices=[('tenis', 'Tênis'), ('sapato', 'Sapato'), ('sandalia', 'Sandália'), ('bota', 'Bota'), ('chinelo', 'Chinelo'), ('sapatilha', 'Sapatilha'), ('outro', 'Outro')],
            ),
        ),
        migrations.AddField(
            model_name='produtocatalogo',
            name='tamanho_calcado',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='produtocatalogo',
            name='categoria',
            field=models.CharField(
                max_length=20,
                choices=[('alimento', 'Alimento'), ('roupa', 'Roupa'), ('calcado', 'Calçado'), ('medicamento', 'Medicamento'), ('outro', 'Outro')],
            ),
        ),
        migrations.AlterField(
            model_name='itemestoque',
            name='categoria',
            field=models.CharField(
                max_length=20,
                choices=[('alimento', 'Alimento'), ('roupa', 'Roupa'), ('calcado', 'Calçado'), ('medicamento', 'Medicamento'), ('outro', 'Outro')],
            ),
        ),
    ]
