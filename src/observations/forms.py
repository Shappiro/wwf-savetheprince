from django.forms import ModelForm

from .models import Site

class SiteForm(ModelForm): # This will generate HTML from the model
    class Meta:
        model = Site
        fields = ('name','regione','provincia','descrizione',)
        #exclude = ["form_user"] # field compiled by default