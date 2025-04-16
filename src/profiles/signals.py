from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import logging
from . import models
from utils.views import send_email

logger = logging.getLogger("project")

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_handler(sender, instance, created, **kwargs):
    if not created:
        return

    def get_or_null(string):
        if string is None or string == '':
            string = 'Non definito'
        else:
            if type(string) == type(True):
                if string:
                    string = 'Sì'
                else:
                    string = 'No'
        return string

    profile = models.Profile(user=instance)
    profile.save()

    subject = 'Save the Prince | Nuovo profilo creato'
    message = """<strong>Messaggio automatico</strong><br>
        L'utente con nome {} si è appena registrato!
        <hr>
        Ricordati di abilitarlo con i dovuti permessi.
        <br>
        <em><a href="https://savetheprince.net">Progetto Save the Prince</a></em></br>
        <image src="https://savetheprince.net/media/admin-interface/logo/logo-big.png" width=200></image></br>
        """.format(get_or_null(instance))

    subject2 = 'Save the Prince | Profilo creato, ora completalo!'
    message2 = """<strong>Messaggio automatico</strong><br>
        Ciao! Abbiamo rilevato la registrazione dell'utente {} sul sito savetheprince.net!
        </br>
        Se la registrazione è legittima, ti chiediamo un ultimo sforzo, ovvero:
        <ul>
            <li> di completare i dati <a href="https://savetheprince.net/utenti/me/edit/">del tuo profilo</a></li>
            <li> sempre nella schermata di completamento del profilo, di scaricare, compilare e caricare una scansione della liberatoria, come indicato nel campo "Liberatoria", se la tua associazione di riferimento la prevede</li>
        </ul>
        <br/>

        Se ritieni che questa mail non sia legittima, ti preghiamo di contattare gli amministratori
        del sito rispondendo a questa mail o scrivendo all'indirizzo <a href="mailto:salvataggioanfibi@gmail.com">salvataggioanfibi@gmail.com</a>
        <br/>
        <br/>
        Nome utente: {}
        <br/>
        Mail: {}
        <br/>
        Form per cambiare la password: <a href="https://savetheprince.net/password-change/">https://savetheprince.net/password-change/</a>
        <br/>
        <br/>
        Grazie,
        <br/>
        Il team <em>savetheprince.net</em>
        <hr>
        <em><a href="https://savetheprince.net">Progetto Save the Prince</a></em></br>
        <image src="https://savetheprince.net/media/admin-interface/logo/logo-big.png" width=40></image></br>
        """.format(get_or_null(instance), get_or_null(instance), get_or_null(instance.email))

    send_email("salvataggioanfibi@gmail.com", "salvataggioanfibi@gmail.com",subject, str(message), message)
    send_email("salvataggioanfibi@gmail.com", instance.email,subject2, str(message2), message2)
    logger.info('Nuovo profilo per {} creato'.format(instance))