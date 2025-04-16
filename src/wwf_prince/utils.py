from imagekit import ImageSpec
from imagekit.processors import ResizeToFill
from imagekit.cachefiles import ImageCacheFile

class AdminThumbnailSpec(ImageSpec):
    processors = [ResizeToFill(90, 60)]
    format = 'JPEG'
    options = {'quality': 60 }

def cached_admin_thumb(instance):
    # `image` is the name of the image field on the model
    cached = ImageCacheFile(AdminThumbnailSpec(instance.image))
    # only generates the first time, subsequent calls use cache
    cached.generate()
    return cached

ABRUZZO = 'Abruzzo'
BASILICATA = 'Basilicata'
CALABRIA = 'Calabria'
CAMPANIA = 'Campania'
EMILIA_ROMAGNA = 'Emilia - Romagna'
FRIULI_VENEZIA_GIULIA = 'Friuli - Venezia Giulia'
LAZIO = 'Lazio'
LIGURIA = 'Liguria'
LOMBARDIA = 'Lombardia'
MARCHE = 'Marche'
MOLISE = 'Molise'
PIEMONTE = 'Piemonte'
PUGLIA = 'Puglia'
SARDEGNA = 'Sardegna'
SICILIA = 'Sicilia'
TOSCANA = 'Toscana'
TRENTINO_ALTO_ADIGE = 'Trentino - Alto Adige'
UMBRIA = 'Umbria' 
VALLE_AOSTA = 'Valle d''Aosta'
VENETO = 'Veneto'

AGRIGENTO = 'Agrigento'
ALESSANDRIA = 'Alessandria'
ANCONA = 'Ancona'
AOSTA = 'Aosta'
AREZZO = 'Arezzo'
ASCOLI_PICENO = 'Ascoli Piceno'
ASTI = 'Asti'
AVELLINO = 'Avellino'
BARI = 'Città Metropolitana di Bari'
BARLETTA_ANDRIA_TRANI = 'Barletta - Andria - Trani'
BELLUNO = 'Belluno'
BENEVENTO = 'Benevento'
BERGAMO = 'Bergamo'
BIELLA = 'Biella'
BOLOGNA = 'Città Metropolitana di Bologna'
BOLZANO = 'Bolzano'
BRESCIA = 'Brescia'
BRINDISI = 'Brindisi'
CALTANISSETTA = 'Caltanissetta'
CAGLIARI = 'Città Metropolitana di Cagliari'
CAMPOBASSO = 'Campobasso'
CASERTA = 'Caserta'
CATANIA = 'Città Metropolitana di Catania'
CATANZARO = 'Catanzaro'
CHIETI = 'Chieti'
COMO = 'Como'
COSENZA = 'Cosenza'
CREMONA = 'Cremona'
CROTONE = 'Crotone'
CUNEO = 'Cuneo'
ENNA = 'Enna'
FERMO = 'Fermo'
FERRARA = 'Ferrara'
FIRENZE = 'Città Metropolitana di Firenze'
FOGGIA = 'Foggia'
FORLI_CESENA = 'Forlì - Cesena'
FROSINONE = 'Frosinone'
GENOVA = 'Città Metropolitana di Genova'
GROSSETO = 'Grosseto'
IMPERIA = 'Imperia'
ISERNIA = 'Isernia'
SPEZIA = 'La Spezia'
AQUILA = 'L''Aquila'
LATINA = 'Latina'
LECCE = 'Lecce'
LECCO = 'Lecco'
LIVORNO = 'Livorno'
LODI = 'Lodi'
LUCCA = 'Lucca'
MACERATA = 'Macerata'
MANTOVA = 'Mantova'
MASSA_CARRARA = 'Massa - Carrara'
MATERA = 'Matera'
MESSINA = 'Città Metropolitana di Messina'
MILANO = 'Città Metropolitana di Milano'
MODENA = 'Modena'
MONZA_BRIANZA = 'Monza e Brianza'
NAPOLI = 'Città Metropolitana di Napoli'
NOVARA = 'Novara'
NUORO = 'Nuoro'
ORISTANO = 'Oristano'
PADOVA = 'Padova'
PALERMO = 'Città Metropolitana di Palermo'
PARMA = 'Parma'
PAVIA = 'Pavia'
PERUGIA = 'Perugia'
PESARO_URBINO = 'Pesaro e Urbino'
PESCARA = 'Pescara'
PIACENZA = 'Piacenza'
PISA = 'Pisa'
PISTOIA = 'Pistoia'
POTENZA = 'Potenza'
PRATO = 'Prato'
RAGUSA = 'Ragusa'
RAVENNA = 'Ravenna'
REGGIO_CALABRIA = 'Città Metropolitana di Reggio Calabria'
REGGIO_EMILIA = 'Reggio Emilia'
RIETI = 'Rieti'
RIMINI = 'Rimini'
ROMA = 'Città Metropolitana di Roma Capitale'
ROVIGO = 'Rovigo'
SALERNO = 'Salerno'
SASSARI = 'Sassari'
SAVONA = 'Savona'
SIENA = 'Siena'
SIRACUSA = 'Siracusa'
SONDRIO = 'Sondrio'
SUD_SARDEGNA = 'Sud Sardegna'
TARANTO = 'Taranto'
TERAMO = 'Teramo'
TERNI = 'Terni'
TORINO = 'Città Metropolitana di Torino'
TRAPANI = 'Trapani'
TRENTO = 'Trento'
TREVISO = 'Treviso'
VARESE = 'Varese'
VENEZIA = 'Città Metropolitana di Venezia'
VERBANO_CUSIO_OSSOLA = 'Verbano - Cusio - Ossola'
VERCELLI = 'Vercelli'
VERONA = 'Verona'
VIBO_VALENTIA = 'Vibo Valentia'
VICENZA = 'Vicenza'
VITERBO = 'Viterbo'

REGIONE_CHOICES = (
    (ABRUZZO,'Abruzzo'),(BASILICATA,'Basilicata'),(CALABRIA,'Calabria'),
    (CAMPANIA,'Campania'),(EMILIA_ROMAGNA,'Emilia - Romagna'),
    (FRIULI_VENEZIA_GIULIA,'Friuli - Venezia Giulia'),(LAZIO,'Lazio'),(LIGURIA,'Liguria'),
    (LOMBARDIA,'Lombardia'),(MARCHE,'Marche'),(MOLISE,'Molise'),
    (PIEMONTE,'Piemonte'),(PUGLIA,'Puglia'),(SARDEGNA,'Sardegna'),
    (SICILIA,'Sicilia'),(TOSCANA,'Toscana'),(TRENTINO_ALTO_ADIGE,'Trentino - Alto Adige'),
    (UMBRIA,'Umbria' ),(VALLE_AOSTA,'Valle d''Aosta'),(VENETO,'Veneto')
)

PROVINCIA_CHOICES = (
    (AGRIGENTO,'Agrigento'),(ALESSANDRIA,'Alessandria'),(ANCONA,'Ancona'),
    (AOSTA,'Aosta'),(AREZZO,'Arezzo'),(ASCOLI_PICENO,'Ascoli Piceno'),
    (ASTI,'Asti'),(AVELLINO,'Avellino'),(BARI,'Città Metropolitana di Bari'),(BARLETTA_ANDRIA_TRANI,'Barletta - Andria - Trani'),
    (BELLUNO,'Belluno'),(BENEVENTO,'Benevento'),(BERGAMO,'Bergamo'),(BOLOGNA,'Città Metropolitana di Bologna'),
    (BIELLA,'Biella'),(BOLZANO,'Bolzano'),(BRESCIA,'Brescia'),
    (BRINDISI,'Brindisi'),(CALTANISSETTA,'Caltanissetta'),
    (CAGLIARI,'Città Metropolitana di Cagliari'),
    (CAMPOBASSO,'Campobasso'),
    (CASERTA,'Caserta'),
    (CATANIA,'Città Metropolitana di Catania'),
    (CATANZARO,'Catanzaro'),(CHIETI,'Chieti'),
    (COMO,'Como'),(COSENZA,'Cosenza'),(CREMONA,'Cremona'),
    (CROTONE,'Crotone'),(CUNEO,'Cuneo'),(ENNA,'Enna'),
    (FERMO,'Fermo'),(FERRARA,'Ferrara'),
    (FIRENZE,'Città Metropolitana di Firenze'),
    (FOGGIA,'Foggia'),
    (FORLI_CESENA,'Forlì - Cesena'),(FROSINONE,'Frosinone'),
    (GENOVA,'Città Metropolitana di Genova'),
    (GROSSETO,'Grosseto'),
    (IMPERIA,'Imperia'),(ISERNIA,'Isernia'),(SPEZIA,'La Spezia'),
    (AQUILA,'L''Aquila'),(LATINA,'Latina'),(LECCE,'Lecce'),
    (LECCO,'Lecco'),(LIVORNO,'Livorno'),(LODI,'Lodi'),
    (LUCCA,'Lucca'),(MACERATA,'Macerata'),(MANTOVA,'Mantova'),
    (MASSA_CARRARA,'Massa - Carrara'),(MATERA,'Matera'),
    (MESSINA,'Città Metropolitana di Messina'),
    (MILANO,'Città Metropolitana di Milano'),
    (MODENA,'Modena'),
    (MONZA_BRIANZA,'Monza e Brianza'),(NOVARA,'Novara'),
    (NAPOLI,'Città Metropolitana di Napoli'),
    (NUORO,'Nuoro'),
    (ORISTANO,'Oristano'),(PADOVA,'Padova'),
    (PALERMO,'Città Metropolitana di Palermo'),
    (PARMA,'Parma'),
    (PAVIA,'Pavia'),(PERUGIA,'Perugia'),(PESARO_URBINO,'Pesaro e Urbino'),
    (PESCARA,'Pescara'),(PIACENZA,'Piacenza'),(PISA,'Pisa'),
    (PISTOIA,'Pistoia'),(POTENZA,'Potenza'),(PRATO,'Prato'),
    (RAGUSA,'Ragusa'),(RAVENNA,'Ravenna'),
    (REGGIO_CALABRIA,'Città Metropolitana di Reggio Calabria'),
    (REGGIO_EMILIA,'Reggio Emilia'),
    (RIETI,'Rieti'),(RIMINI,'Rimini'),
    (ROMA,'Città Metropolitana di Roma Capitale'),
    (ROVIGO,'Rovigo'),
    (SALERNO,'Salerno'),(SASSARI,'Sassari'),(SAVONA,'Savona'),
    (SIENA,'Siena'),(SIRACUSA,'Siracusa'),(SONDRIO,'Sondrio'),
    (SUD_SARDEGNA,'Sud Sardegna'),(TARANTO,'Taranto'),(TERAMO,'Teramo'),
    (TERNI,'Terni'),
    (TORINO,'Città Metropolitana di Torino'),
    (TRAPANI,'Trapani'),(TRENTO,'Trento'),
    (TREVISO,'Treviso'),(VARESE,'Varese'),(VENEZIA,'Città Metropolitana di Venezia'),(VERBANO_CUSIO_OSSOLA,'Verbano - Cusio - Ossola'),
    (VERCELLI,'Vercelli'),(VERONA,'Verona'),(VIBO_VALENTIA,'Vibo Valentia'),(VICENZA,'Vicenza'),
    (VITERBO,'Viterbo'),
)