# Generated by Django 2.1.2 on 2018-10-24 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20181024_0826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='association',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.Association'),
        ),
    ]
