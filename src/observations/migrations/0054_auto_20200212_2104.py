# Generated by Django 2.1.2 on 2020-02-12 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0053_auto_20200212_2058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='volontari_key',
        ),
        migrations.AddField(
            model_name='anagraficavolontari',
            name='session',
            field=models.ManyToManyField(blank=True, to='observations.Session', verbose_name='Sessioni alle quali il volontario ha partecipato'),
        ),
    ]
