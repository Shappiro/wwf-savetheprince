from django.contrib.gis.db import models
from rest_framework.fields import ChoiceField
from tinymce.models import HTMLField
from ordered_model.models import OrderedModel
from django.forms import TextInput

FAQ_TYPES = [
    ('generali','FAQ generali'),
    ('volontari','FAQ per i volontari'),
    ('referenti','FAQ per i referenti')
]

class ShortTextField(models.TextField):
    def formfield(self, **kwargs):
        kwargs.update(
            {"widget": TextInput(attrs={'size': 40})}
        )
        return super(ShortTextField, self).formfield(**kwargs)
class FAQModel(OrderedModel):
    """
    Domande e risposte per la sezione FAQ
    """
    question = HTMLField("Domanda")
    answer = HTMLField("Risposta")
    faqtype = models.CharField("Categoria",max_length=128,choices=FAQ_TYPES,default='volontari')

    class Meta:
        verbose_name = 'Domanda con risposta'
        verbose_name_plural = 'Domande e risposte'


class Regioni(models.Model):
    regione = models.CharField("Nome",primary_key=True,max_length=512)
    regioni_id = models.IntegerField("ID",db_column="id")
    cod_reg = models.CharField("Codice",blank=True,null=True,max_length=512)
    geom = models.PolygonField("Geometria",srid=3035)

    class Meta:
        managed = False
        db_table = 'env_data\".\"regioni'
        verbose_name = 'Regione'
        verbose_name_plural = 'Regioni'
        ordering =  ['regione']
        
    
    def __str__(self):
        return "{}".format(self.regione)

class Province(models.Model):
    provincia = models.CharField("Nome",primary_key=True,max_length=512)
    province_id = models.IntegerField("ID",db_column="id")
    cod_reg = models.CharField("Codice regione",blank=True,null=True,max_length=512)
    cod_prov = models.CharField("Codice provincia",blank=True,null=True,max_length=512)
    geom = models.PolygonField("Geometria",srid=3035)

    class Meta:
        managed = False
        db_table = 'env_data\".\"province'
        verbose_name = 'Provincia'
        verbose_name_plural = 'Province'
        ordering =  ['provincia']
    
    def __str__(self):
        if self.cod_prov:
            return "{} ({})".format(self.provincia,self.cod_prov)
        else:
            return "{}".format(self.provincia)
        

class ComuniManager(models.Manager):
    def for_user(self,user):
        return super(ComuniManager, self).get_queryset_set().filter(comune__isnull=False)

class Comuni(models.Model):
    comune = models.CharField("Comune",primary_key=True,max_length=512)
    comuni_id = models.IntegerField("ID",db_column="id")
    cod_reg = models.CharField("Codice regione",blank=True,null=True,max_length=512)
    cod_prov = models.CharField("Codice provincia",blank=True,null=True,max_length=512)
    geom = models.MultiPolygonField("Geometria",srid=3035)
    objects = ComuniManager()
    class Meta:
        managed = False
        db_table = 'env_data\".\"comuni'
        verbose_name = 'Comune'
        verbose_name_plural = 'Comuni'
        ordering =  ['comune']
    
    def __str__(self):
        if self.cod_prov:
            return "{} ({})".format(self.comune,self.cod_prov)
        else:
            return "{}".format(self.comune)