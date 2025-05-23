# Generated by Django 2.2 on 2020-02-25 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0077_auto_20200225_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='observationdetail',
            name='indet_ritorno',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Numero indeterminati vivi in ritorno'),
        ),
        migrations.AlterField(
            model_name='observationdetail',
            name='indet_andata',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Numero indeterminati vivi in andata'),
        ),
    ]
