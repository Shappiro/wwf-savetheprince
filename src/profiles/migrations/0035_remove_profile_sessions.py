# Generated by Django 2.1.2 on 2020-02-13 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0034_auto_20200213_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='sessions',
        ),
    ]
