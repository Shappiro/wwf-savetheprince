from __future__ import unicode_literals
from six import python_2_unicode_compatible
import uuid
from django.contrib.gis.db import models
from profiles.models import *
from django.conf import settings
from italian_utils.utils import REGIONI
from tinymce.models import HTMLField
from sorl.thumbnail import ImageField
from phonenumber_field.modelfields import PhoneNumberField

from wwf_prince.utils import *
from observations.models import Site, Session
from wwf_prince.models import TimeStampedModel
from utils.views import send_email

class Association(models.Model):
    name = models.CharField("Associazione", primary_key=True,max_length=300)
    slug = models.UUIDField(default=uuid.uuid4, blank=True,editable=False)
    image = ImageField('Logo', upload_to='logo/%Y-%m-%d/', null=True,blank=True)
    region = models.CharField("Regione", max_length=40, null=True,blank=True, choices=REGIONE_CHOICES)
    province = models.CharField("Provincia o Città Metropolitana", max_length=40, null=True,blank=True, choices=PROVINCIA_CHOICES)
    descrizione = HTMLField("Descrizione", max_length=10000, blank=True,null=True,help_text="Una breve descrizione della storia e scopi dell'Associazione")
    email = models.EmailField("Mail",max_length=1024,default="salvataggioanfibi@gmail.com")
    website = models.URLField("WWW", max_length=300,blank=True, null=True)
    facebook = models.URLField("FB", max_length=300,blank=True, null=True)
    modello_liberatoria = models.FileField('Modello di liberatoria', upload_to='liberatorie/MODELLI/', null=True,blank=True)
    #reference = models.ForeignKey('Profile', models.SET_NULL,verbose_name="Volontari registrati (CON PROFILO SU SAVE THE PRINCE)",blank=True,null=True)

    class Meta:
        managed = True
        verbose_name = 'Associazione'
        verbose_name_plural = 'Associazioni'

    def __str__(self):
        if self.region:
            return "{} ({})".format(self.name, self.region)
        else:
            return "{}".format(self.name)


VOLONTARIO = 'volunteer'
REFERENTE_SITO = 'reference-site'
REFERENTE_ASSOCIAZIONE = 'reference-organization'
ADMIN = 'admin'
ROLE_CHOICES = (
    (VOLONTARIO, 'Volontaria/o'),
    (REFERENTE_SITO, 'Referente sito'),
    (REFERENTE_ASSOCIAZIONE, 'Referente Associazione'),
    (ADMIN, 'Amministratore generale'),
)

def liberatoria_upload(instance, filename):
    return 'liberatorie/{0}'.format(filename.encode("ascii", "ignore").decode().replace(' ','_'))

class BaseProfile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,primary_key=True)
    profile_name = models.CharField("Nome", max_length=400)
    profile_surname = models.CharField("Cognome", max_length=400)
    slug = models.UUIDField(default=uuid.uuid4, blank=True, editable=False)
    picture = ImageField('Immagine di profilo', upload_to='profile_pics/%Y-%m-%d/',null=True, blank=True)
    bio = HTMLField("Bio", blank=True, null=True)
    role = models.CharField("Ruolo", max_length=400,choices=ROLE_CHOICES, default=VOLONTARIO)
    role_descr = models.CharField("Ruolo esteso", max_length=400, blank=True, null=True)
    email_verified = models.BooleanField("Email verificata?", default=False)
    association = models.ForeignKey(Association, on_delete=models.CASCADE,blank=True, null=True, verbose_name='Associazione')
    association_verified = models.BooleanField("Associazione verificata?",default=False)
    province = models.CharField("Provincia o Città Metropolitana", max_length=40, null=True,blank=True, choices=PROVINCIA_CHOICES)
    phone_number = PhoneNumberField("Telefono", null=True, blank=True)
    province_verified = models.BooleanField("Provincia verificata?",default=False)
    profile_show = models.BooleanField("Vuoi che il tuo profilo appaia nelle liste di volontari per i siti?", default=False)
    phone_show = models.BooleanField("Vuoi che il tuo numero di telefono sia visibile agli altri volontari?", default=False)
    mail_show = models.BooleanField("Vuoi che la tua mail sia visibile agli altri volontari?", default=False)
    update_mail_receive = models.BooleanField("Vuoi ricevere una mail di riassunto ogni volta che inserisci una sessione di salvataggio?", default=False)
    preferred_site = models.ForeignKey(Site, verbose_name="Indica il tuo sito di salvataggio preferito", on_delete=models.SET_NULL, null=True,related_name='profile_preferred_site')
    #preferred_sites = models.ManyToManyField(Site, verbose_name="Indica i tuoi siti di salvataggio preferiti", blank=True,null=True,related_name='profile_preferred_sites')
    liberatoria = models.FileField('Liberatoria', upload_to=liberatoria_upload,null=True, blank=True)

    __original_mode = None # Un check giusto per mandare mail solo in caso di invio di NUOVA liberatoria

    def __init__(self, *args, **kwargs):
        super(BaseProfile, self).__init__(*args, **kwargs)
        self.__original_mode = self.liberatoria

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.liberatoria != self.__original_mode:
            message = """<strong>Messaggio automatico</strong><br>
            L'utente {} {} ha caricato / modificato la liberatoria!<br>
            Per abilitarlo e/o aggiornarne il profilo, clicca <a href="https://savetheprince.net/admin/authtools/user/{}/change/">qui</a>.
            <hr>
            <em><a href="https://savetheprince.net">Progetto Save the Prince</a></em>
            <br>
            <image src="https://savetheprince.net/media/loghi/orizzontale/logo_orizzontale_nero.png" width=200></image><br>
            """.format(self.profile_name,self.profile_surname,self.pk)
            send_email("salvataggioanfibi@gmail.com", "salvataggioanfibi@gmail.com",
            "L'utente {} {} ha caricato / modificato la liberatoria!".format(self.profile_name,self.profile_surname), str(message), message)
            self.__original_mode = self.liberatoria
        else:
            pass

        super(BaseProfile, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_mode = self.liberatoria

    class Meta:
        abstract = True
        verbose_name = 'Profilo utente'
        verbose_name_plural = 'Profili utente'


#@python_2_unicode_compatible
class Profile(BaseProfile):
    def __str__(self):
        return "{} ({})".format(self.user, self.province)

    def get_references(self):
        if self.association:
            return Profile.objects.exclude(user=self.user).filter(association__name=self.association.name, role__in=['reference-site', 'reference-organization']).order_by('role')

    def get_reference_organization(self):
        if self.association:
            q = Profile.objects.exclude(user=self.user).filter(association__name=self.association.name, role__in=['reference-organization']).order_by('role')
            if q and set(q)!=set(self.get_own_site_reference()): # set is w/o ordering, list takes order into
                return q 
            else:
                return None 

    def get_reference_other_organization(self):
        if self.association:
            return Profile.objects.exclude(association=self.association).filter(role__in=['reference-organization']).exclude(user=self.user).order_by('profile_name')

    def get_own_site_reference(self):
        if self.association:
            q = Profile.objects.filter(association=self.association,role__in=['reference-site'],preferred_site=self.preferred_site).exclude(user=self.user).order_by('profile_name')
            if q:
                return q 
            else:
                a = Profile.objects.exclude(user=self.user).filter(association__name=self.association.name, role__in=['reference-organization']).order_by('role')
                if a:
                    return a 
                else:
                    return Profile.objects.filter(profile_name__in=['Aaron','Stefania'],profile_surname__in=['Iemma','Dal Pra'])

    def get_volunteers_allsites(self):
        if self.association and self.role:
            if self.role!='volunteer':
                profiles = Profile.objects.filter(association__name=self.association.name).exclude(role__in=['reference-site', 'reference-organization']).exclude(user=self.user).order_by('role')
                return profiles
            else:
                return None

    def get_volunteers_mysite(self):
        if self.association and self.role:
            if self.role!='volunteer':
                profiles = Profile.objects.filter(association__name=self.association.name,preferred_site=self.preferred_site).exclude(role__in=['reference-site', 'reference-organization']).exclude(user=self.user).order_by('user__name')
                return profiles
            else:
                return None

    def check_liberatoria_upload(self):
        """
        Ciao!
        vista la tua registrazione al portale Save the Prince (savetheprince.net), pensiamo... che potresti essere interessat* ad entrare a far parte ufficialmente di un gruppo di salvataggio! :)
        A questo scopo e per far sì che il tuo profilo sul portale venga attivato, abbiamo bisogno che tu inserisca la liberatoria debitamente sottoscritta entro il tuo profilo, oppure che la invii all'indirizzo salvataggioanfibi@gmail.com.
        
        Sempre a questo indirizzo, puoi scriverci per qualsiasi altro dubbio: non esitare a contattarci, per iniziare a prender parte a questa entusiasmante e tutto sommato semplice attività!

        Ti aspettiamo nei nostri gruppi di volontari!

        A presto
        Il Team di Save the Prince 

        NB: qualora entro 15 giorni non ricevessimo alcuna risposta il tuo account verrà automaticamente cancellato dal sistema e per riaccedervi dovrai effettuare una nuova registrazione        
        """
        if not self.liberatoria and timezone.now() > self.date_joined + timedelta(days=15):
            message = """<strong>Messaggio automatico</strong><br>
            L'utente {} {} non ha caricato la liberatoria entro 15 giorni dal primo accesso.<br>
            <hr>
            <em><a href="https://savetheprince.net">Progetto Save the Prince</a></em>
            <br>
            <image src="https://savetheprince.net/media/loghi/orizzontale/logo_orizzontale_nero.png" width=200></image><br>
            """.format(self.profile_name, self.profile_surname)
            send_email(
                "salvataggioanfibi@gmail.com", "salvataggioanfibi@gmail.com",
                "L'utente {} {} non ha ancora caricato la liberatoria".format(self.profile_name, self.profile_surname), str(message), message
            )


#@receiver(post_save, sender=Profile)
#def check_liberatoria_upload(sender, instance, **kwargs):
#    instance.check_liberatoria_upload()

class FreeProfile(models.Model):
    """
    Magazzino di dati e delle liberatorie per le/i volontar* non registrat*
    """
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    profile_name = models.CharField("Nome", max_length=400)
    profile_surname = models.CharField("Cognome", max_length=400)
    role = models.CharField("Ruolo", max_length=400,choices=ROLE_CHOICES, default=VOLONTARIO)
    role_descr = models.CharField("Ruolo esteso", max_length=400, blank=True, null=True)
    email = models.EmailField("Email", blank=True,null=True)
    email_verified = models.BooleanField("Email verificata?", default=True)
    association = models.ForeignKey(Association, on_delete=models.CASCADE, verbose_name='Associazione')
    association_verified = models.BooleanField("Associazione verificata?",
                                               default=True)
    province = models.CharField("Provincia o Città Metropolitana", max_length=40, null=True,
                                blank=True, choices=PROVINCIA_CHOICES)
    phone_number = PhoneNumberField("Telefono", null=True, blank=True)
    province_verified = models.BooleanField("Provincia verificata?",
                                            default=True)
    profile_show = models.BooleanField(
        "Vuoi che il profilo appaia nelle liste di volontari per i siti?", default=False)
    phone_show = models.BooleanField(
        "Vuoi che il numero di telefono sia visibile agli altri volontari?", default=False)
    mail_show = models.BooleanField(
        "Vuoi che la mail sia visibile agli altri volontari?", default=False)
    preferred_site = models.ForeignKey(
        Site, verbose_name="Sito di salvataggio preferito", on_delete=models.SET_NULL, null=True,blank=True)
    liberatoria = models.FileField('Liberatoria', upload_to='liberatorie/%Y-%m-%d/')

    class Meta:
        verbose_name = 'Dati di un* volontari* non registrat*'
        verbose_name_plural = 'Dati dei/delle volontari* non registrat*'

    def __str__(self):
        return "{} {} ({})".format(self.profile_name, self.profile_surname,self.province)

