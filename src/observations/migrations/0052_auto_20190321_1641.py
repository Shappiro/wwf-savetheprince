# Generated by Django 2.1.2 on 2019-03-21 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0051_sitesummary'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sitesummary',
            options={'managed': False, 'verbose_name': 'Riassunti per sito', 'verbose_name_plural': 'Riassunti per i siti'},
        ),
    ]
