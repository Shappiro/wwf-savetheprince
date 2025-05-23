# Generated by Django 2.2 on 2020-02-29 13:01

from django.db import migrations, models
import django.db.models.deletion
import observations.models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0089_auto_20200229_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specieimage',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, help_text='Immagini rappresentative della specie', null=True, upload_to=observations.models.specieimage_upload_function, verbose_name='Immagine'),
        ),
        migrations.CreateModel(
            name='SpecieDoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1200, verbose_name='Titolo documento')),
                ('doc', models.FileField(help_text='Documento utile per la specie', upload_to=observations.models.speciedoc_upload_function, verbose_name='Documento')),
                ('doctype', models.CharField(choices=[('Identificazione specie', 'Identificazione specie'), ('Altro', 'Altro')], max_length=300, verbose_name='Tipo documento')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Data di produzione del documento')),
                ('author', models.CharField(blank=True, max_length=300, null=True, verbose_name='Autore')),
                ('specie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sitedocs', to='observations.Specie')),
            ],
            options={
                'verbose_name': 'Documento della specie',
                'verbose_name_plural': 'Documenti della specie',
            },
        ),
    ]
