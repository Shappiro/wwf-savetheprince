# Generated by Django 2.1.2 on 2018-10-27 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0010_auto_20181027_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specie',
            name='image',
            field=models.ImageField(blank=True, help_text='Una immagine rappresentativa della specie', null=True, upload_to='species/%Y-%m-%d/', verbose_name='Immagine'),
        ),
    ]
