# Generated by Django 2.2 on 2021-06-06 14:47

from django.db import migrations, models
import observations.models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0124_auto_20210606_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='effort',
            field=models.IntegerField(blank=True, null=True, verbose_name='Sforzo, in minuti'),
        ),
        migrations.AlterField(
            model_name='specieimage',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, help_text='Immagini rappresentative della specie', null=True, upload_to=observations.models.specieimage_upload_function, verbose_name='Immagine'),
        ),
    ]
