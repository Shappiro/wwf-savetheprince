# Generated by Django 2.1.4 on 2018-12-10 14:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0040_auto_20181210_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='begin',
            field=models.TimeField(default=datetime.datetime(2018, 12, 10, 14, 4, 30, 752837, tzinfo=utc), verbose_name='Inizio'),
        ),
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 12, 10, 14, 4, 30, 752785, tzinfo=utc), verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='session',
            name='end',
            field=models.TimeField(default=datetime.datetime(2018, 12, 10, 14, 4, 30, 752865, tzinfo=utc), verbose_name='Fine'),
        ),
    ]
