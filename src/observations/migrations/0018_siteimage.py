# Generated by Django 2.1.2 on 2018-10-28 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0017_auto_20181028_1049'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Immagini rappresentative del sito', null=True, upload_to='sites/%Y-%m-%d/', verbose_name='Immagine')),
                ('date', models.DateField(auto_now=True)),
                ('author', models.CharField(blank=True, max_length=300, null=True, verbose_name='Autore')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='siteimages', to='observations.Site')),
            ],
            options={
                'verbose_name': 'Immagine del sito',
                'verbose_name_plural': 'Immagini del sito',
                'abstract': False,
            },
        ),
    ]
