# Generated by Django 2.2 on 2022-03-26 19:24

from django.db import migrations, models
import observations.models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0147_auto_20220326_1115'),
    ]

    operations = [
        migrations.RenameField(
            model_name='siteimage',
            old_name='type',
            new_name='typeimg',
        ),
        migrations.AlterField(
            model_name='session',
            name='volontari_free',
            field=models.ManyToManyField(blank=True, to='profiles.FreeProfile', verbose_name='Volontari non registrati, con liberatoria'),
        ),
        migrations.AlterField(
            model_name='specieimage',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, help_text='Immagini rappresentative della specie', null=True, upload_to=observations.models.specieimage_upload_function, verbose_name='Immagine'),
        ),
    ]
