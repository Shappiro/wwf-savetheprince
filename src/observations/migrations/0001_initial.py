# Generated by Django 2.1.2 on 2018-10-24 08:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('specie', models.CharField(blank=True, max_length=300, null=True, verbose_name='Nome scientifico')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='species/%Y-%m-%d/', verbose_name='Species')),
                ('vernacular_it', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome italiano')),
                ('vernacular_en', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome inglese')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrizione')),
                ('iucn', models.URLField(blank=True, max_length=300, null=True, verbose_name='IUCN')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
