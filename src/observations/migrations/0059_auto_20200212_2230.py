# Generated by Django 2.1.2 on 2020-02-12 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0058_auto_20200212_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anagraficavolontari',
            name='provincia',
            field=models.CharField(blank=True, choices=[('Agrigento', 'Agrigento'), ('Alessandria', 'Alessandria'), ('Ancona', 'Ancona'), ('Aosta', 'Aosta'), ('Arezzo', 'Arezzo'), ('Ascoli Piceno', 'Ascoli Piceno'), ('Asti', 'Asti'), ('Avellino', 'Avellino'), ('Barletta - Andria - Trani', 'Barletta - Andria - Trani'), ('Belluno', 'Belluno'), ('Benevento', 'Benevento'), ('Bergamo', 'Bergamo'), ('Biella', 'Biella'), ('Bolzano', 'Bolzano'), ('Brescia', 'Brescia'), ('Brindisi', 'Brindisi'), ('Caltanissetta', 'Caltanissetta'), ('Campobasso', 'Campobasso'), ('Caserta', 'Caserta'), ('Catanzaro', 'Catanzaro'), ('Chieti', 'Chieti'), ('Como', 'Como'), ('Cosenza', 'Cosenza'), ('Cremona', 'Cremona'), ('Crotone', 'Crotone'), ('Cuneo', 'Cuneo'), ('Enna', 'Enna'), ('Fermo', 'Fermo'), ('Ferrara', 'Ferrara'), ('Foggia', 'Foggia'), ('Forlì - Cesena', 'Forlì - Cesena'), ('Frosinone', 'Frosinone'), ('Grosseto', 'Grosseto'), ('Imperia', 'Imperia'), ('Isernia', 'Isernia'), ('La Spezia', 'La Spezia'), ('LAquila', 'LAquila'), ('Latina', 'Latina'), ('Lecce', 'Lecce'), ('Lecco', 'Lecco'), ('Livorno', 'Livorno'), ('Lodi', 'Lodi'), ('Lucca', 'Lucca'), ('Macerata', 'Macerata'), ('Mantova', 'Mantova'), ('Massa - Carrara', 'Massa - Carrara'), ('Matera', 'Matera'), ('Modena', 'Modena'), ('Monza e Brianza', 'Monza e Brianza'), ('Novara', 'Novara'), ('Nuoro', 'Nuoro'), ('Oristano', 'Oristano'), ('Padova', 'Padova'), ('Parma', 'Parma'), ('Pavia', 'Pavia'), ('Perugia', 'Perugia'), ('Pesaro e Urbino', 'Pesaro e Urbino'), ('Pescara', 'Pescara'), ('Piacenza', 'Piacenza'), ('Pisa', 'Pisa'), ('Pistoia', 'Pistoia'), ('Potenza', 'Potenza'), ('Prato', 'Prato'), ('Ragusa', 'Ragusa'), ('Ravenna', 'Ravenna'), ('Reggio Emilia', 'Reggio Emilia'), ('Rieti', 'Rieti'), ('Rimini', 'Rimini'), ('Rovigo', 'Rovigo'), ('Salerno', 'Salerno'), ('Sassari', 'Sassari'), ('Savona', 'Savona'), ('Siena', 'Siena'), ('Siracusa', 'Siracusa'), ('Sondrio', 'Sondrio'), ('Sud Sardegna', 'Sud Sardegna'), ('Taranto', 'Taranto'), ('Teramo', 'Teramo'), ('Terni', 'Terni'), ('Trapani', 'Trapani'), ('Trento', 'Trento'), ('Treviso', 'Treviso'), ('Varese', 'Varese'), ('Verbano - Cusio - Ossola', 'Verbano - Cusio - Ossola'), ('Vercelli', 'Vercelli'), ('Verona', 'Verona'), ('Vibo Valentia', 'Vibo Valentia'), ('Vicenza', 'Vicenza'), ('Viterbo', 'Viterbo')], max_length=35, null=True, verbose_name='Provincia'),
        ),
        migrations.AlterField(
            model_name='anagraficavolontari',
            name='regione',
            field=models.CharField(blank=True, choices=[('Abruzzo', 'Abruzzo'), ('Basilicata', 'Basilicata'), ('Calabria', 'Calabria'), ('Campania', 'Campania'), ('Emilia - Romagna', 'Emilia - Romagna'), ('Friuli - Venezia Giulia', 'Friuli - Venezia Giulia'), ('Lazio', 'Lazio'), ('Liguria', 'Liguria'), ('Lombardia', 'Lombardia'), ('Marche', 'Marche'), ('Molise', 'Molise'), ('Piemonte', 'Piemonte'), ('Puglia', 'Puglia'), ('Sardegna', 'Sardegna'), ('Sicilia', 'Sicilia'), ('Toscana', 'Toscana'), ('Trentino - Alto Adige', 'Trentino - Alto Adige'), ('Umbria', 'Umbria'), ('Valle dAosta', 'Valle dAosta'), ('Veneto', 'Veneto')], max_length=35, null=True, verbose_name='Regione'),
        ),
    ]
