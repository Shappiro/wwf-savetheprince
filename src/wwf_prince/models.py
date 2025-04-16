from django.contrib.gis.db import models
from django.db.models import Aggregate, CharField, Value
import re
import uuid

from django.conf import settings
from crum import get_current_user
from django.forms import TextInput

from django.conf import settings
from django.contrib.gis.gdal import CoordTransform, SpatialReference
from django.utils import timezone


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        """ Quando l'elemento viene salvato, aggiorna il timestamp """
        if not self.pk:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(TimeStampedModel, self).save(*args, **kwargs)

class UserReferencedModel(models.Model):
    """
    Una classe di modelli astratta che permette al modello
    di registrare automaticamente utente inseritore e modificatore
    """
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Aggiunto da",
                                   null=True, blank=True, on_delete=models.SET_NULL, editable=False, related_name="%(class)s_added_related")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Modificato da",
                                    null=True, blank=True, on_delete=models.SET_NULL, editable=False, related_name="%(class)s_modified_related")

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(UserReferencedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True

