# Generated by Django 2.1.2 on 2018-12-27 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0017_auto_20181227_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='region',
            field=models.CharField(blank=True, choices=[('Abruzzo', 'Abruzzo'), ('Basilicata', 'Basilicata'), ('Calabria', 'Calabria'), ('Campania', 'Campania'), ('Emilia - Romagna', 'Emilia - Romagna'), ('Friuli - Venezia Giulia', 'Friuli - Venezia Giulia'), ('Lazio', 'Lazio'), ('Liguria', 'Liguria'), ('Lombardia', 'Lombardia'), ('Marche', 'Marche'), ('Molise', 'Molise'), ('Piemonte', 'Piemonte'), ('Puglia', 'Puglia'), ('Sardegna', 'Sardegna'), ('Sicilia', 'Sicilia'), ('Toscana', 'Toscana'), ('Trentino - Alto Adige', 'Trentino - Alto Adige'), ('Umbria', 'Umbria'), ('Valle dAosta', 'Valle dAosta'), ('Veneto', 'Veneto')], max_length=40, null=True, verbose_name='Regione'),
        ),
        migrations.AlterField(
            model_name='association',
            name='region',
            field=models.CharField(blank=True, choices=[('Abruzzo', 'Abruzzo'), ('Basilicata', 'Basilicata'), ('Calabria', 'Calabria'), ('Campania', 'Campania'), ('Emilia - Romagna', 'Emilia - Romagna'), ('Friuli - Venezia Giulia', 'Friuli - Venezia Giulia'), ('Lazio', 'Lazio'), ('Liguria', 'Liguria'), ('Lombardia', 'Lombardia'), ('Marche', 'Marche'), ('Molise', 'Molise'), ('Piemonte', 'Piemonte'), ('Puglia', 'Puglia'), ('Sardegna', 'Sardegna'), ('Sicilia', 'Sicilia'), ('Toscana', 'Toscana'), ('Trentino - Alto Adige', 'Trentino - Alto Adige'), ('Umbria', 'Umbria'), ('Valle dAosta', 'Valle dAosta'), ('Veneto', 'Veneto')], max_length=40, null=True, verbose_name='Regione'),
        ),
    ]
