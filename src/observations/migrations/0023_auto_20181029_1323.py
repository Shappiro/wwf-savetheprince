# Generated by Django 2.1.2 on 2018-10-29 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0022_auto_20181029_1306'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='observation',
            options={'verbose_name': 'Osservazione', 'verbose_name_plural': 'Osservazioni'},
        ),
        migrations.AddField(
            model_name='session',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='site',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='specie',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='specie',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='Data'),
        ),
    ]
