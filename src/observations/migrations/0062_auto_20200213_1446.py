# Generated by Django 2.1.2 on 2020-02-13 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0035_remove_profile_sessions'),
        ('observations', '0061_auto_20200213_1418'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='site',
            options={'ordering': ['name'], 'verbose_name': 'Sito di salvataggio', 'verbose_name_plural': 'Siti di salvataggio'},
        ),
        migrations.AddField(
            model_name='session',
            name='volontari',
            field=models.ManyToManyField(blank=True, null=True, to='profiles.Profile', verbose_name='Volontari registrati'),
        ),
    ]
