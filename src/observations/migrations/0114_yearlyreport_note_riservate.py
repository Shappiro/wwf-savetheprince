# Generated by Django 2.2 on 2021-05-21 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0113_auto_20210513_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='yearlyreport',
            name='note_riservate',
            field=models.TextField(blank=True, help_text='Queste note sono disponibili ai soli referenti: campo utile per inserire informazioni sensibili', null=True, verbose_name='Note riservate'),
        ),
    ]
