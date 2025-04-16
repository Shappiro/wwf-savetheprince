from __future__ import unicode_literals

import os
import uuid
import datetime
from itertools import chain

from admin_log.models import AdminLogMixin
from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
# from django.core.mail import send_mail
from django.db.models import F, Func, Value, Sum, Count
from django.db.models.signals import (post_delete, post_save, pre_delete,
                                      pre_save)
from django.dispatch import receiver
from django.utils import timezone
#ofrom django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe
from queryable_properties.properties.base import queryable_property
from sorl.thumbnail import ImageField
from tinymce.models import HTMLField

from utils.models import ShortTextField  # , Regioni, Province
from wwf_prince.models import TimeStampedModel, UserReferencedModel
from wwf_prince.utils import *



class Specie(TimeStampedModel):
    """
    Memorizza informazioni sulle varie specie
    """
    id = models.UUIDField(default=uuid.uuid4, blank=True,
                          editable=False, primary_key=True)
    specie = models.CharField("Nome scientifico", max_length=300,
                              null=True, blank=True)
    specie_connected = models.ManyToManyField('Specie', related_name='specieconnected',verbose_name="Specie con le quali può essere confusa",blank=True)
    vernacular_it = models.CharField("Nome italiano", max_length=100,null=True, blank=True, help_text="Nome comune italiano")
    vernacular_en = models.CharField("Nome inglese", max_length=100,blank=True, null=True, help_text="Nome comune inglese")
    description = HTMLField("Descrizione", blank=True, null=True)
    iucn = models.URLField("IUCN", max_length=300, blank=True, null=True,
                           help_text="URL della pagina IUCN della specie")
    wiki = models.URLField("Wiki", max_length=300, blank=True, null=True,
                           help_text="URL della pagina Wikipedia della specie")

    class Meta:
        abstract = False
        ordering = ('specie',)
        verbose_name = 'Specie'
        verbose_name_plural = 'Specie'

    def __str__(self):
        return "{} ({})".format(self.specie, self.vernacular_it)

    def name_lower(self):
        return "{}".format(self.specie.lower().replace(' ', '_').replace("'", '').replace("(", '_').replace(")", '_').replace(".", ''))

    def immagine(self):
        img = self.specieimages.first()
        if img is None:
            return
        else:
            return mark_safe("<img src='{}/{}' width=150,height=150 />"
                             .format(settings.MEDIA_URL, img.image))


def specieimage_upload_function(instance, filename):
    """ this function has to return the location to upload the file """

    return os.path.join('species/%s/images/' % instance.specie.specie, filename)


class SpecieImage(models.Model):
    specie = models.ForeignKey(Specie, related_name='specieimages',on_delete=models.CASCADE,verbose_name='Specie')
    image = ImageField('Immagine',upload_to=specieimage_upload_function,null=True,blank=True,help_text="Immagini rappresentative della specie")
    author = models.CharField("Autore", max_length=300, null=True, blank=True)

    class Meta:
        verbose_name = 'Immagine della specie'
        verbose_name_plural = 'Immagini della specie'

    def __str__(self):
        if self.image:
            if self.author:
                return "Immagine di {} - (c) {}".format(self.specie.vernacular_it, self.author)
            else:
                return "Immagine di {}".format(self.specie.vernacular_it)
        else:
            return "Immagine non presente! Ricaricarla"


    def url(self):
        if self.image:
            return self.image.url
        else:
            return None

SPECIEDOC_CHOICES = (
    ('Identificazione specie', 'Identificazione specie'),
    ('Disambiguazione specie', 'Disambiguazione specie'),
    ('Altro', 'Altro'),
)


def speciedoc_upload_function(instance, filename):
    """ this function has to return the location to upload the file """

    return os.path.join('species/%s/docs/' % instance.specie.specie, filename)

class SpecieDoc(models.Model):
    title = models.CharField("Titolo documento", max_length=1200)
    specie = models.ForeignKey(Specie, related_name='speciedocs',on_delete=models.CASCADE,verbose_name='Specie')
    doc = models.FileField('Documento',upload_to=speciedoc_upload_function,help_text="Documento utile per la specie")
    doctype = models.CharField("Tipo documento", max_length=300, choices=SPECIEDOC_CHOICES)
    date = models.DateField("Data di produzione del documento", blank=True, null=True)
    author = models.CharField("Autore", max_length=300, null=True, blank=True)

    def __str__(self):
        return "Documento per la specie {} - {}".format(self.specie.specie,
                                                        self.author)

    class Meta:
        verbose_name = 'Documento della specie'
        verbose_name_plural = 'Documenti della specie'


class SiteManager(models.Manager):
    """
    Se l'utente non è un superutente, 
    allora non viene data la possibilità di 
    vedere siti non attivi
    """
    def for_user(self, user):
        if self.user.is_superuser:
            return super(SiteManager, self).get_queryset_set().all()
        else:
            return super(SiteManager, self).get_queryset_set().filter(attivo=True)

def flyer_upload_function(instance, filename):
    """
    La funzione ritorna il percorso alla cartella
    nella quale effettuare l'upload
    del file del flyer
    """
    return os.path.join('sites/%s/' % instance.name, filename)

class Site(AdminLogMixin, TimeStampedModel):
    """
    Informazioni sul sito di salvataggio
    """
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField("Nome", blank=True, null=True, max_length=300,help_text="Nome identificativo del sito. Deve essere studiato in modo da poter essere riconosciuto da chiunque")
    regione = models.CharField("Regione", max_length=64, blank=True,null=True, choices=REGIONE_CHOICES)
    provincia = models.CharField("Provincia", max_length=64, blank=True,null=True, choices=PROVINCIA_CHOICES)
    comune = models.CharField("Comune", max_length=100, blank=True, null=True)
    descrizione = HTMLField("Descrizione", blank=True, null=True)
    attivo = models.BooleanField("Attivo?", default=True)
    flyer = ImageField('Flyer avviso',upload_to=flyer_upload_function,null=True,blank=True,help_text="Flyer di avviso attraversamento anfibi")
    geom = models.LineStringField("Strada", srid=4326, blank=True, null=True)
    meteoblue_widget = ShortTextField("Widget MeteoBlue",blank=True,null=True)
    lunghezza = models.IntegerField("Lunghezza",blank=True,null=True)

    objects = SiteManager()

    @property
    def latitude(self):
        return self.geom.centroid.coords[0]

    @property
    def longitude(self):
        return self.geom.centroid.coords[1]

    def __str__(self):
        return "{} ({} - {})".format(self.name,
                                     self.regione, self.provincia)

    @property
    def name_lower(self):
        return "{}".format(self.name.lower().replace(' ', '_').replace("'", '').replace("(", '_').replace(")", '_').replace(".", '_'))

    def immagine(self):
        img = self.siteimages.first()
        if img is None:
            return
        else:
            return mark_safe("<img src='{}/{}' width=150,height=150 />"
                             .format(settings.MEDIA_URL, img.image))

    class Meta:
        ordering = ['name']
        verbose_name = 'Sito di salvataggio'
        verbose_name_plural = 'Siti di salvataggio'

class SiteVolunteers(models.Model):
    id = models.AutoField("ID",primary_key=True)
    profile = models.ForeignKey('profiles.Profile',models.CASCADE,verbose_name="Profilo volontario")
    sites = models.ManyToManyField(Site,verbose_name="Siti")

    class Meta:
        managed = True
        ordering = ['profile', ]
        verbose_name = 'Siti preferiti dai volontari'
        verbose_name_plural = 'Siti di salvataggio per i volontari'
    
    def __str__(self):
        return "Siti per volontario {}".format(self.profile.profile_name)

SITEDOC_CHOICES = (
    ('Report / Riassunto', 'Report / Riassunto'),
    ('Descrizione', 'Descrizione'),
    ('Altro', 'Altro'),
)
def sitedoc_upload_function(instance, filename):
    return os.path.join('sites/%s/docs/' % instance.title, filename)

class SiteDoc(models.Model):
    title = models.CharField("Titolo documento", max_length=1200)
    site = models.ForeignKey(Site, related_name='sitedocs',on_delete=models.CASCADE,verbose_name='Sito di salvataggio')
    doc = models.FileField('Documento',upload_to=sitedoc_upload_function,help_text="Documento utile per il sito")
    doctype = models.CharField("Tipo documento", max_length=300, choices=SITEDOC_CHOICES)
    date = models.DateField("Data di produzione del documento", blank=True, null=True)
    author = models.CharField("Autore", max_length=300, null=True, blank=True)

    def __str__(self):
        if self.author:
            return "Documento per il sito {} ({})".format(self.site.name,self.author)
        else:
            return "Documento per il sito {}".format(self.site.name)
    class Meta:
        verbose_name = 'Documento del sito di salvataggio'
        verbose_name_plural = 'Documenti associati ai siti di salvataggio'


class SiteSummary(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField("Nome sito", blank=True, null=True,db_column="sitename", max_length=50)
    year = models.IntegerField("Anno", blank=True, null=True)
    specie = models.TextField("Specie", blank=True, null=True, max_length=40)
    sex = models.TextField("Sesso", blank=True, null=True, max_length=10)
    alive = models.BooleanField("Vivo?", default=True)
    direction = models.TextField(
        "Direzione", blank=True, null=True, max_length=10)
    n = models.IntegerField("Numero", blank=True, null=True)

    class Meta:
        managed = False
        ordering = ['-year']
        ordering = ['-year','specie','sex','direction','alive','n']
        verbose_name = 'Riassunti per sito'
        verbose_name_plural = 'Riassunti per i siti'
        db_table = 'sitesummary'

SITEIMAGE_CHOICES = (
    ('Inquadramento', 'Inquadramento'),
    ('Sito riproduttivo', 'Sito riproduttivo'),
    ('Sito di svernamento', 'Sito di svernamento'),
    ('Barriere', 'Barriere'),
    ('Volontari', 'Volontari'),
    ('Condizioni', 'Condizioni'),
    ('Mortalità', 'Mortalità'),
    ('Altro', 'Altro'),
)

def image_upload_function(instance, filename):
    """ this function has to return the location to upload the file """
    return os.path.join('sites/%s/images/' % instance.site.name, filename)

class SiteImage(models.Model):
    site = models.ForeignKey(Site,related_name='siteimages',on_delete=models.CASCADE,verbose_name='Sito di salvataggio')
    image = ImageField('Immagine',upload_to=image_upload_function,null=True,blank=True,help_text="Immagini rappresentative del sito")
    typeimg = models.CharField("Tipo immagine", max_length=300, choices=SITEIMAGE_CHOICES)
    date = models.DateField(auto_now=True)
    author = models.CharField("Autore", max_length=300, null=True, blank=True)

    class Meta:
        verbose_name = 'Immagine del sito'
        verbose_name_plural = 'Immagini del sito'

    def __str__(self):
        if self.image:
            if self.author:
                return "Immagine del sito {} ({}) - (c) {}".format(self.site.name,self.site.regione, self.author)
            else:
                return "Immagine del sito {} ({})".format(self.site.name,self.site.regione)
        else:
                return "Immagine non presente! Ricaricarla"

def doc_upload_function(instance, filename):
    """ this function has to return the location to upload the file """

    return os.path.join('sites/%s/docs/' % instance.site.name, filename)

class Session(AdminLogMixin, TimeStampedModel):
    """
    Informazioni generiche riguardo una sessione di salvataggio
    """

    SERENO = 'M-SER'
    VARIABILE = 'M-VAR'
    NUVOLOSO = 'M-NUV'
    PIOGGIA = 'M-PIO'
    NEVE = 'M-NEV'
    NEBBIA = 'M-NEBPIO'
    WIND_POCO = 'V-LOW'
    WIND_MEDIO = 'V-MED'
    WIND_FORTE = 'V-HIG'
    WIND_NULL = 'V-NO'
    METEO_CHOICES = (
        (NUVOLOSO, 'Nuvoloso'),
        (PIOGGIA, 'Pioggia'),
        (VARIABILE, 'Variabile'),
        (SERENO, 'Sereno'),
        (NEBBIA, 'Pioggerella/Nebbia'),
        (NEVE, 'Neve'),
    )
    WIND_CHOICES = (
        (WIND_NULL, 'Assente'),
        (WIND_POCO, 'Scarso'),
        (WIND_MEDIO, 'Medio'),
        (WIND_FORTE, 'Intenso')
    )

    id = models.AutoField("ID", editable=False, primary_key=True)
    site = models.ForeignKey(Site, blank=True, null=True, on_delete=models.CASCADE,related_name='sites', verbose_name='Sito di salvataggio')
    date = models.DateField("Data", default=timezone.now)
    ended_next_day = models.BooleanField("Terminato il giorno dopo?", default=False)
    begin = models.TimeField("Ora d'inizio")
    end = models.TimeField("Ora di fine")
    meteo = models.CharField("Meteo", max_length=15,choices=METEO_CHOICES, null=True, blank=True)
    vento = models.CharField("Vento", max_length=15,choices=WIND_CHOICES, null=True, blank=True)
    temperature = models.FloatField("Temperatura (locale)", help_text='La temperatura media in gradi centigradi registrata durante il monitoraggio, direttamente sul sito', null=True, blank=True)
    temperature_interpolated = models.FloatField("Temperatura (da meteo)", help_text='La temperatura media in gradi centigradi segnata dalla centrale meteo più vicina durante il periodo di monitoraggio', null=True, blank=True)
    volontari = models.ManyToManyField('profiles.Profile', verbose_name="Volontari registrati (CON PROFILO SU SAVE THE PRINCE)", blank=True,null=True,help_text="Iniziare a digitare un nome, quindi ->>>CLICCARE<<<- sul nome che si desidera aggiungere")
    volontari_unregistered = models.CharField(
        "Volontari non registrati (SENZA PROFILO SU SAVE THE PRINCE)", help_text="Iniziali maiuscole, separare con virgola un volontario dall'altro", max_length=2046, null=True, blank=True)
    note = models.TextField("Note", null=True, blank=True)
    effort = models.IntegerField("Sforzo, in minuti",blank=True,null=True)
    class Meta:
        ordering = ('-date','-begin','site')
        verbose_name = 'Uscita di salvataggio'
        verbose_name_plural = 'Uscite di salvataggio'

    def clean(self):
        # The call to super().clean() ensures that any validation logic in parent classes is maintained. If your form inherits another that doesn’t return a cleaned_data dictionary in its clean() method (doing so is optional), then don’t assign cleaned_data to the result of the super() call and use self.cleaned_data instead:
        super(Session,self).clean()  
        if self.end and self.begin:
            if self.end < self.begin and not self.ended_next_day:
                raise ValidationError({
                    'end': "L'ora di fine non può essere precedente all'ora di inizio (a meno che il salvataggio non sia terminato il giorno dopo)!"
                })
        else:
            raise ValidationError({
                'start': "Devi inserire l'ora di fine e l'ora di inizio, nel formato corretto!",
                'end': "Devi inserire l'ora di fine e l'ora di inizio, nel formato corretto!",
            })
            
        #if not self.volontari and not self.volontari_unregisterd:
        #    raise ValidationError({
        #        'volontari': "Questo campo (oppure il campo 'Volontari non registrati') deve essere compilato!",
        #        'volontari_unregistered': "Questo campo (oppure il campo 'Volontari registrati') deve essere #compilato!"
        #    })
            

    def __str__(self):
        return "{} - {}, dalle {} alle {}".format(self.site, self.date,
                                                  self.begin, self.end)

    @property
    def volontari_count(self):
        if self.volontari:
            return self.volontari.count()

    @property
    def volontari_unregistered_count(self):
        if self.volontari_unregistered:
            return len(self.volontari_unregistered.split(',')) # returns 1 if there is no comma

    @queryable_property
    def eff(self):
        """
        Gets daily effort as n_volunteers * minutes
        """
        end = self.end
        begin = self.begin

        time_delta = datetime.datetime.combine(self.date,end) - datetime.datetime.combine(self.date,begin)
        total_seconds = time_delta.total_seconds()
        minutes = round(total_seconds/60)
        volontari_registered = self.volontari_count
        volontari_unregistered = self.volontari_unregistered_count

        allvol = sum(filter(None, [volontari_registered,volontari_unregistered]))
        if allvol==0:
            allvol = 1

        return minutes*allvol

    def save(self, *args, **kwargs):
    #    """
    #    Aggiungi effort al salvataggio
    #    """
        if not self.id:
            super(Session, self).save(*args, **kwargs)
        self.effort = self.eff
        super(Session, self).save(*args, **kwargs)

class SessionImage(models.Model):
    session = models.ForeignKey(Session, related_name='sessionimages',on_delete=models.CASCADE,verbose_name='Uscita di salvataggio')
    image = ImageField('Immagine',upload_to='sessions/%Y-%m-%d/',null=True,blank=True,help_text="Immagini dellaa sessione")
    descr = ShortTextField("Descrizione eventuale",blank=True,null=True)
    author = models.CharField("Autorice/autore", max_length=300, null=True, blank=True)

    class Meta:
        verbose_name = 'Immagine della sessione'
        verbose_name_plural = 'Immagini della sessione'

    def __str__(self):
        if self.author:
            return "Immagine della sessione {} ({}) - (c) {}".format(self.session.id,self.session.site, self.author)
        else:
            return "Immagine della sessione {} ({})".format(self.session.id,self.session.site)

    def url(self):
        if self.image:
            return self.image.url
        else:
            return None

class Observation(AdminLogMixin, TimeStampedModel):
    """
    Osservazione di un gruppo omogeneo di individui
    """

    MASCHIO = 'M'
    FEMMINA = 'F'
    INDETERMINATO = 'IND'
    GIOVANE = 'JUV'
    ADULTO = 'AD'
    NEOMETAMORFOSATO = 'NEO'
    ANDATA = 'AND'
    RITORNO = 'RIT'
    VIVI = 'VIV'
    MORTI = 'MOR'
    SEX_CHOICES = (
        (MASCHIO, 'Maschio'),
        (FEMMINA, 'Femmina'),
        (INDETERMINATO, 'Indeterminato'),
    )
    STATE_CHOICES = (
        (NEOMETAMORFOSATO, 'Neometamorfosato'),
        (GIOVANE, 'Giovane'),
        (ADULTO, 'Adulto'),
    )
    DIRECTION_CHOICES = (
        (ANDATA, 'Andata'),
        (RITORNO, 'Ritorno'),
        (INDETERMINATO, 'Indeterminata')
    )
    LIFE_CHOICES = (
        (VIVI, 'Vivi'),
        (MORTI, 'Morti')
    )   
    id = models.UUIDField(default=uuid.uuid4, blank=True,editable=False, primary_key=True)
    specie = models.ForeignKey(Specie, on_delete=models.DO_NOTHING, null=True, blank=True,verbose_name='Specie')
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, related_name='observations', null=True, blank=True,verbose_name='Uscita di salvataggio')
    n = models.PositiveIntegerField("Numero individui", default=0)
    sex = models.CharField("Sesso", null=True, blank=True,choices=SEX_CHOICES, max_length=15)
    state = models.CharField("Stadio vitale", null=True, blank=True,default="Adulto", choices=STATE_CHOICES, max_length=15)
    direction = models.CharField("Direzione", null=True, blank=True, choices=DIRECTION_CHOICES,max_length=15)
    life = models.BooleanField("Vivi?", default=True)

    class Meta:
        managed = False
        verbose_name = 'Osservazione'
        verbose_name_plural = 'Osservazioni'
        db_table = 'observations_exploded'
        ordering = ['-session__date','specie__specie','state','direction','life','n']

    def __str__(self):
        if self.life:
            return "{} {} viv* di {}".format(self.n, self.sex, self.specie.vernacular_it)
        else:
            return "{} {} mort* di {}".format(self.n, self.sex, self.specie.vernacular_it)

class ObservationDetail(AdminLogMixin, TimeStampedModel):
    POCHI = 'pochi'
    MEDI = 'medi'
    MOLTI = 'molti'
    MOLTISSIMI = 'moltissimi'
    NEOMET_CHOICES = (
        (POCHI, '<10'),
        (MEDI, '10-100'),
        (MOLTI, '100-1000'),
        (MOLTISSIMI, '>1000')
    )    
    id = models.UUIDField(default=uuid.uuid4, blank=True,
                          editable=False, primary_key=True)
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE, related_name='observationdetail_specie',verbose_name='Specie')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='observationdetail_session',verbose_name='Uscita di salvataggio')

    alive_female_andata = models.PositiveIntegerField("Numero femmine vive in andata", blank=True, null=True)
    alive_female_ritorno = models.PositiveIntegerField("Numero femmine vive in ritorno", blank=True, null=True)
    alive_female_indet = models.PositiveIntegerField("Numero femmine in direzione indeterminata", blank=True, null=True)

    alive_male_ritorno = models.PositiveIntegerField("Numero maschi vivi in ritorno", blank=True, null=True)
    alive_male_andata = models.PositiveIntegerField("Numero maschi vivi in andata", blank=True, null=True)
    alive_male_indet = models.PositiveIntegerField("Numero maschi in direzione indeterminata", blank=True, null=True)

    alive_indet_andata = models.PositiveIntegerField("Numero indeterminati vivi in andata", blank=True, null=True)
    alive_indet_ritorno = models.PositiveIntegerField("Numero indeterminati vivi in ritorno", blank=True, null=True)
    alive_indet_indet = models.PositiveIntegerField("Numero indeterminati vivi in direzione indeterminata", blank=True, null=True)

    dead_female = models.PositiveIntegerField("Numero femmine morte", blank=True, null=True)
    dead_male = models.PositiveIntegerField("Numero maschi morti", blank=True, null=True)
    dead_indet = models.PositiveIntegerField("Numero indeterminati morti", blank=True, null=True)

    neometamorfosati_vivi_stima = models.CharField("Stima numero neometamorfosati vivi", blank=True, null=True,choices=NEOMET_CHOICES,max_length=128)
    neometamorfosati_morti_stima = models.CharField("Stima numero neometamorfosati morti", blank=True, null=True,choices=NEOMET_CHOICES,max_length=128)
    neometamorfosati_vivi = models.IntegerField("Numero approssimativo neometamorfosati vivi", blank=True, null=True)
    neometamorfosati_morti = models.IntegerField("Numero approssimativo neometamorfosati morti", blank=True, null=True)
    
    giovani = models.PositiveIntegerField("Numero giovani", blank=True, null=True)        

    malati = models.IntegerField("Numero esemplari sospetti malati", blank=True, null=True)
    malati_descrizione = models.TextField("Descrizione esemplari", blank=True, null=True)
    malati_analisi = models.BooleanField("Raccolti campioni per l'analisi?", blank=True, null=True)
    malati_analisi_invio = models.BooleanField("Inviati campioni per l'analisi?", blank=True, null=True)
    malati_conferma = models.BooleanField("Malattia confermata?", blank=True, null=True)
    
    class Meta:
        verbose_name = 'Dettaglio per una specie'
        verbose_name_plural = 'Dettagli per le specie'

    def clean(self):
        super(ObservationDetail,self).clean()
        if self.specie and (
            not self.alive_female_andata and not self.alive_female_ritorno and not self.alive_female_indet and not self.alive_male_andata and not self.alive_male_ritorno and not self.alive_male_indet and not self.alive_indet_andata and not self.alive_indet_ritorno and not self.alive_indet_indet and not self.dead_female and not self.dead_male and not self.dead_indet and not self.neometamorfosati_vivi_stima and not self.neometamorfosati_morti_stima and not self.neometamorfosati_vivi and not self.neometamorfosati_morti and not self.giovani       
        ):
            raise ValidationError({
                'specie': "Stai inserendo una specie, quindi devi inserirne almeno un dato!"
            })

class ObservationDetailImage(models.Model):
    observationdetail = models.ForeignKey(ObservationDetail, related_name='observationdetailimages', on_delete=models.CASCADE, verbose_name="Specie in una sessione")
    image = ImageField('Immagine',upload_to='journals/%Y-%m-%d/',help_text="Immagine del giornale")
    descr = ShortTextField("Descrizione eventuale",blank=True,null=True)
    author = models.CharField("Autorice/autore", max_length=300, null=True, blank=True)

    def __str__(self):
        return "Immagine per la specie {} della sessione {}".format(self.observationdetail.specie, self.observationdetail.session)

    class Meta:
        verbose_name = 'Immagine di una specie particolare nella sessione'
        verbose_name_plural = 'Immagini di una specie particolare nella sessione'



class JournalImage(models.Model):
    journal = models.CharField("Giornale", max_length=300)
    regione = models.CharField("Regione", max_length=64, blank=True,null=True, choices=REGIONE_CHOICES)
    provincia = models.CharField("Provincia", max_length=64, blank=True,null=True, choices=PROVINCIA_CHOICES)
    site = models.ForeignKey(Site, related_name='journalimages',on_delete=models.CASCADE, blank=True, null=True, verbose_name="Sito di salvataggio")
    image = ImageField('Immagine',upload_to='journals/%Y-%m-%d/',help_text="Immagine del giornale")
    date = models.DateField("Data di pubblicazione", blank=True, null=True)
    link = models.URLField("Link all'articolo online", max_length=256, null=True, blank=True)

    def __str__(self):
        return "Immagine di un articolo - {} del {}".format(self.journal, self.date)

    class Meta:
        verbose_name = 'Articolo di giornale'
        verbose_name_plural = 'Articoli di giornale'
        ordering = ["-date"]

class YearlyReport(AdminLogMixin, TimeStampedModel):

    date_begin = models.DateField("Data di inizio dell'attività dei volontari")
    date_end = models.DateField("Data di fine dell'attività dei volontari")
    date_barriers_begin = models.DateField("Data di posa delle barriere, se presenti",blank=True,null=True)
    date_barriers_end = models.DateField("Data di rimozione delle barriere, se presenti",blank=True,null=True)
    site = models.ForeignKey(Site,on_delete=models.CASCADE, blank=True, null=True, verbose_name="Sito di salvataggio")
    year = models.IntegerField("Anno",default=2021)
    andamento = models.TextField("Andamento generale della migrazione",blank=True,null=True)
    note_sito = models.TextField("Note relative alla gestione del sito di salvataggio",blank=True,null=True)
    note_traffico = models.TextField("Note relative al traffico veicolare",blank=True,null=True)
    note_fauna = models.TextField("Note relative alle particolarità faunistiche",blank=True,null=True)
    problematiche = models.TextField("Problematiche generali",blank=True,null=True)
    note_altro = models.TextField("Altre segnalazioni",blank=True,null=True)
    note_riservate = models.TextField("Note riservate",blank=True,null=True,help_text="Queste note sono disponibili ai soli referenti campo utile per inserire informazioni sensibili")

    n_volontari = models.IntegerField("Numero di volontari",editable=False,default=1)
    n_uscite = models.IntegerField("Numero di uscite",editable=False,default=1)
    specie_toexclude = models.ManyToManyField(Specie,related_name='specie_toexclude',blank=True,null=True,verbose_name="Specie da escludere dai report")
    
    def __str__(self):
        return "Report del {} del sito {}".format(self.year, self.site.name)

    class Meta:
        verbose_name = 'Report annuale'
        verbose_name_plural = 'Report annuali'
        unique_together = ('site', 'year',)
        ordering = ['-year','site']

    @property
    def volunteers_count(self):
        session = Session.objects.filter(site=self.site,date__year=self.year)

        volontari_registered = sum([b.volontari.count() for b in session.filter(volontari__isnull=False)])
        volontari_unregistered = len(list(chain.from_iterable([b.volontari_unregistered.split(',') for b in session.filter(volontari_unregistered__isnull=False)])))
        volontari_none = len(session.filter(volontari__isnull=True,volontari_unregistered__isnull=True))

        allvol = sum(filter(None, [volontari_registered,volontari_unregistered,volontari_none]))
        if allvol:
            return allvol 
        else:
            return 1

    @property 
    def excluded_species(self):
        excluded_species = list(YearlyReport.objects.filter(site=self.site,year=self.year).values_list('specie_toexclude__specie',flat=True))
        if len(excluded_species) > 0:
            return excluded_species
        else:
            return None

    @property
    def volunteers_single_count(self):
        queryset = Session.objects.filter(site=self.site,date__year=self.year)

        volontari_unregistered = queryset.values_list('volontari_unregistered',flat=True).distinct()
        volontari_unregistered = len(set([item for subquery in [volontari.split(',') for volontari in volontari_unregistered if volontari] for item in subquery]))
        volontari_registered = len(set([item.values('user__name').distinct()[0]["user__name"] for item in [ v.volontari.all() for v in queryset] if item]))

        if sum(filter(None, [volontari_registered,volontari_unregistered])):
            return sum(filter(None, [volontari_registered,volontari_unregistered]))
        else:
            return None

    @property
    def volunteers_names(self):
        queryset = Session.objects.filter(site=self.site,date__year=self.year)

        volontari_unregistered = queryset.values_list('volontari_unregistered',flat=True).distinct()
        volontari_unregistered = set([item for subquery in [volontari.split(',') for volontari in volontari_unregistered if volontari] for item in subquery])
        volontari_registered = set([item.values('user__name').distinct()[0]["user__name"] for item in [ v.volontari.all() for v in queryset] if item])
        allvol = list(volontari_registered) + list(volontari_unregistered)
        allvol.sort()        
        return ", ".join(allvol)
    
    @property
    def sessions_count(self):
        return Session.objects.filter(site=self.site,date__year=self.year).count()

    @property
    def giovani_count(self):
        queryset = SiteSummary.objects.filter(name=self.site.name,year=self.year)
        juveniles = {}
        if queryset:
            specie = list(set(queryset.values_list('specie',flat=True)))
            specie.sort()
            for spec in specie:
                n = sum([0 if el is None else el for el in list(ObservationDetail.objects.filter(session__in=Session.objects.filter(site=self.site,date__year=self.year),specie=Specie.objects.filter(specie=spec)[0]).values_list('giovani',flat=True))])  
                if n>0:
                    juveniles[spec] = n
        if len(juveniles):
            return juveniles
        else:
            return None

    @property
    def contacted_species(self):
        queryset = SiteSummary.objects.filter(name=self.site.name)#,year=self.year)
        if queryset:
            specie = list(set(queryset.values_list('specie',flat=True)))
            specie.sort()
            excluded = self.excluded_species
            if excluded:
                specie = [x for x in specie if x not in excluded]
            return specie
        else:
            return None
    @property
    def species_sexratio(self):
        queryset = SiteSummary.objects.filter(name=self.site.name,year=self.year)
        if queryset:
            specie = list(set(queryset.values_list('specie',flat=True)))
            specie.sort()
            excluded = self.excluded_species
            if excluded:
                specie = [x for x in specie if x not in excluded]
            ratios = {}
            for spec in specie:
                male = queryset.filter(specie=spec,sex='M')
                if male:
                    male = male.aggregate(Sum('n'))["n__sum"] 
                female = queryset.filter(specie=spec,sex='F')
                if female:
                    female = female.aggregate(Sum('n'))["n__sum"] 
                if(male and female):
                    ratios[spec] = round(female/male,4)
            return ratios
        else:
            return None
    
    
    @property
    def contacted_species_formatted(self):
        queryset = SiteSummary.objects.filter(name=self.site.name)#,year=self.year)
        
        if queryset:
            specie = [x for x in list(set(queryset.values_list('specie',flat=True)))]#if x!='Salamandra salamandra']
            specie.sort()
            excluded = self.excluded_species
            if excluded:
                specie = [x for x in specie if x not in excluded]            
            allspec = zip(specie,[x.lower().replace('.','').replace(' ','_') for x in specie])
            return allspec
        else:
            return None

    def save(self, *args, **kwargs):
        self.n_volontari = self.volunteers_count
        self.n_uscite = self.sessions_count
        return super(YearlyReport, self).save(*args, **kwargs)

def specieimage_upload_function(instance, filename):
    """ this function has to return the location to upload the file """

    return os.path.join('species/%s/images/' % instance.specie.specie, filename)


def yearlyreportimage_upload_function(instance, filename):
    return 'sites/{}/images/report_{}/{}'.format( 
        instance.yearly_report.site.name,
        instance.yearly_report.year,
        filename
    )

class YearlyReportImage(models.Model):
    yearly_report = models.ForeignKey(YearlyReport, related_name='yearlyreportimages',
                               on_delete=models.CASCADE,verbose_name='Immagini report annuale')
    image = ImageField('Immagine',
                       upload_to=yearlyreportimage_upload_function,
                       null=True,
                       blank=True,
                       help_text="Immagini rappresentative dell'anno di monitoraggio")
    descr = ShortTextField("Descrizione eventuale",blank=True,null=True)
    author = models.CharField("Autorice/autore", max_length=300, null=True, blank=True)
   
    class Meta:
        verbose_name = 'Immagine della annata di monitoraggio'
        verbose_name_plural = 'Immagini della annata di monitoraggio'

    def __str__(self):
        if self.image:
            if self.author:
                return "Immagine del sito {} per l'anno {} - (c) {}".format(self.yearly_report.site.name,self.yearly_report.year, self.author)
            else:
                return "Immagine del sito {} per l'anno {}".format(self.yearly_report.site.name,self.yearly_report.year)
        else:
            return "Immagine non presente! Ricaricarla"

    def url(self):
        if self.image:
            return self.image.url
        else:
            return None

class Pond(AdminLogMixin, TimeStampedModel):
    """
    Informazioni sui punti di possibile tutela
    (piccole pozze dove gli anfibi si riproducono)
    """
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField("Nome", blank=True, null=True, max_length=300,
                            help_text="Nome identificativo del punto di possibile tutela.")
    regione = models.CharField("Regione", max_length=64, blank=True, null=True, choices=REGIONE_CHOICES)
    provincia = models.CharField("Provincia", max_length=64, blank=True, null=True, choices=PROVINCIA_CHOICES)
    comune = models.CharField("Comune", max_length=100, blank=True, null=True)
    descrizione = HTMLField("Descrizione", blank=True, null=True,
                            help_text="Descrizione")
    attivo = models.BooleanField("Attivo?", default=True)
    geom = models.PolygonField("Area", srid=4326, blank=True, null=True)
    lunghezza = models.IntegerField("Lunghezza, se rilevante", blank=True, null=True)
    data_scoperta = models.DateField("Data del primo rilevamento", blank=True, null=True)
    species = models.ManyToManyField(Specie, related_name='ponds', verbose_name='Specie osservate', blank=True, null=True)
    tutelato = models.BooleanField("Tutelato?", default=False)
    proprietario = models.CharField("Proprietario", max_length=300, blank=True, null=True)
    contatto_proprietario = models.CharField("Contatto proprietario", max_length=300, blank=True, null=True)
    
    def __str__(self):
        return "{} ({} - {})".format(self.name, self.regione, self.provincia)

    @property
    def latitude(self):
        return self.geom.centroid.coords[0]

    @property
    def longitude(self):
        return self.geom.centroid.coords[1]

    def immagine(self):
        img = self.pondimages.first()
        if img is None:
            return
        else:
            return mark_safe("<img src='{}/{}' width=150,height=150 />"
                             .format(settings.MEDIA_URL, img.image))

    class Meta:
        ordering = ['name']
        verbose_name = 'Punto di possibile tutela'
        verbose_name_plural = 'Punti di possibile tutela'

class PondMonitor(AdminLogMixin, TimeStampedModel):
    """
    Monitoraggio di un punto di possibile tutela
    """
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    pond = models.ForeignKey(Pond, on_delete=models.CASCADE, related_name='pondmonitors', verbose_name='Punto di possibile tutela')
    date = models.DateField("Data", default=timezone.now)
    time = models.TimeField("Ora d'inizio")
    end = models.TimeField("Ora di fine")
    meteo = models.CharField("Meteo", max_length=15, choices=Session.METEO_CHOICES, null=True, blank=True)
    vento = models.CharField("Vento", max_length=15, choices=Session.WIND_CHOICES, null=True, blank=True)
    temperature = models.FloatField("Temperatura (locale)", help_text='La temperatura media in gradi centigradi registrata durante il monitoraggio, direttamente sul sito', null=True, blank=True)
    volontari = models.ManyToManyField('profiles.Profile', verbose_name="Volontari registrati (CON PROFILO SU SAVE THE PRINCE)", blank=True,null=True,help_text="Iniziare a digitare un nome, quindi ->>>CLICCARE<<<- sul nome che si desidera aggiungere")
    volontari_unregistered = models.CharField(
        "Volontari non registrati (SENZA PROFILO SU SAVE THE PRINCE)", help_text="Iniziali maiuscole, separare con virgola un volontario dall'altro", max_length=2046, null=True, blank=True)
    note = models.TextField("Note", null=True, blank=True)
    species = models.ManyToManyField(Specie, related_name='pondmonitors', verbose_name='Specie osservate', blank=True, null=True)

    class Meta:
        ordering = ('-date','-time','pond')
        verbose_name = 'Monitoraggio del punto di possibile tutela'
        verbose_name_plural = 'Monitoraggi dei punti di possibile tutela'

class PondImages(models.Model):
    pond = models.ForeignKey('Pond', related_name='pondimages', on_delete=models.CASCADE, verbose_name='Punto di possibile tutela')
    image = ImageField('Immagine', upload_to='ponds/%Y-%m-%d/', null=True, blank=True,
                       help_text="Immagine rappresentativa del punto di possibile tutela")
    descr = ShortTextField("Descrizione eventuale", blank=True, null=True)
    author = models.CharField("Autore", max_length=300, null=True, blank=True)

    class Meta:
        verbose_name = 'Immagine del punto di possibile tutela'
        verbose_name_plural = 'Immagini dei punti di possibile tutela'

    def __str__(self):
        if self.image:
            if self.author:
                return "Immagine del punto di possibile tutela {} - (c) {}".format(self.pond.name, self.author)
            else:
                return "Immagine del punto di possibile tutela {}".format(self.pond.name)
        else:
            return "Immagine non presente! Ricaricala"

    def url(self):
        if self.image:
            return self.image.url
        else:
            return None