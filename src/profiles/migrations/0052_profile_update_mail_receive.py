# Generated by Django 2.2 on 2022-04-26 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0051_auto_20220421_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='update_mail_receive',
            field=models.BooleanField(default=False, verbose_name='Vuoi ricevere una mail di riassunto ogni volta che inserisci una sessione di salvataggio?'),
        ),
    ]
