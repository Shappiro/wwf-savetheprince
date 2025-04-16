from __future__ import unicode_literals
#from django.utils.encoding import python_2_unicode_compatible
import uuid
from django.db import models
from django.conf import settings
from italian_utils.utils import REGIONI
from tinymce.models import HTMLField
from sorl.thumbnail import ImageField

from profiles.models import Association
from observations.models import Site

from wwf_prince.models import TimeStampedModel

class Post(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    date = models.DateField("Data di pubblicazione",auto_now=True)
    title = models.CharField("Titolo",default="Una notizia!",blank=True,null=True,max_length=200)
    new = HTMLField("Corpo",blank=True,null=True)
    association = models.ForeignKey(Association,blank=True,null=True,
        on_delete=models.DO_NOTHING,verbose_name='Associazione di riferimento')
    author_id = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL,editable=False,
                                null=True,blank=True,verbose_name="Pubblicatore")
    site = models.ForeignKey(Site,on_delete=models.SET_NULL,null=True,blank=True,
        verbose_name='Sito di salvataggio')

    class Meta:
        verbose_name = 'Novità'
        verbose_name_plural = 'Novità'
        ordering = ["-date"]

    def __str__(self):
        if self.association:
            return "{} - {} ({}) ".format(self.date,self.title,
                self.association.name)
        else: 
            return "{} - {}".format(self.date,self.title)

