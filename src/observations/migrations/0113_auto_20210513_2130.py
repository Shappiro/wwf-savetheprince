# Generated by Django 2.2 on 2021-05-13 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0112_auto_20210511_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yearlyreport',
            name='date_barriers_begin',
            field=models.DateField(blank=True, null=True, verbose_name='Data di posa delle barriere, se presenti'),
        ),
        migrations.AlterField(
            model_name='yearlyreport',
            name='date_barriers_end',
            field=models.DateField(blank=True, null=True, verbose_name='Data di rimozione delle barriere, se presenti'),
        ),
        migrations.AlterField(
            model_name='yearlyreport',
            name='date_begin',
            field=models.DateField(verbose_name="Data di inizio dell'attività dei volontari"),
        ),
        migrations.AlterField(
            model_name='yearlyreport',
            name='date_end',
            field=models.DateField(verbose_name="Data di fine dell'attività dei volontari"),
        ),
    ]
