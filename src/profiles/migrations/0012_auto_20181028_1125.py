# Generated by Django 2.1.2 on 2018-10-28 11:25

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_auto_20181028_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='profile_pics/%Y-%m-%d/', verbose_name='Immagine di profilo'),
        ),
    ]
