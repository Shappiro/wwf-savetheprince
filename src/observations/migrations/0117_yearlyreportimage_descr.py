# Generated by Django 2.2 on 2021-05-22 07:32

from django.db import migrations
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0116_auto_20210522_0909'),
    ]

    operations = [
        migrations.AddField(
            model_name='yearlyreportimage',
            name='descr',
            field=utils.models.ShortTextField(blank=True, null=True, verbose_name='Descrizione eventuale'),
        ),
    ]
