# Generated by Django 2.1.3 on 2018-11-28 15:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0033_auto_20181101_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='begin',
            field=models.TimeField(default=datetime.datetime(2018, 11, 28, 15, 39, 56, 330762, tzinfo=utc), verbose_name='Inizio'),
        ),
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 11, 28, 15, 39, 56, 330727, tzinfo=utc), verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='session',
            name='end',
            field=models.TimeField(default=datetime.datetime(2018, 11, 28, 15, 39, 56, 330789, tzinfo=utc), verbose_name='Fine'),
        ),
    ]
