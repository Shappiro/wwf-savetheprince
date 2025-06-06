# Generated by Django 2.2 on 2022-02-19 10:30

import admin_log.fields
import admin_log.middleware
from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import observations.models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0137_auto_20220219_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='session',
            name='created_by',
            field=admin_log.fields.AutoCreatedByField(blank=True, default=admin_log.middleware.AdminLogMiddleware.get_user_id, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AlterField(
            model_name='session',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='session',
            name='modified_by',
            field=admin_log.fields.AutoModifiedByField(blank=True, default=admin_log.middleware.AdminLogMiddleware.get_user_id, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modified by'),
        ),
        migrations.AlterField(
            model_name='specieimage',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, help_text='Immagini rappresentative della specie', null=True, upload_to=observations.models.specieimage_upload_function, verbose_name='Immagine'),
        ),
    ]
