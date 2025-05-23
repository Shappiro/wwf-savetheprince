# Generated by Django 2.2 on 2022-01-23 09:07

from django.db import migrations
import observations.models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0126_auto_20220123_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specieimage',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, help_text='Immagini rappresentative della specie', null=True, upload_to=observations.models.specieimage_upload_function, verbose_name='Immagine'),
        ),
    ]
