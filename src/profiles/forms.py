from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        #self.helper["id_password"] = ''
        self.helper.layout = Layout(
            Field('name'),
        )

    class Meta:
        model = User
        fields = ['name']


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('picture'),
            Div(
                Div('phone_number', css_class='col-xs-12'),
                css_class="row"),
            Div(
                Div('association', css_class='col-xs-4'),
                Div('province', css_class='col-xs-4'),
                Div('liberatoria', css_class="col-xs-4"),
                css_class="row"),
            Div(
                Div('profile_show', css_class='col-xs-3'),
                Div('mail_show', css_class='col-xs-3'),
                Div('phone_show', css_class='col-xs-3'),
                Div('update_mail_receive', css_class='col-xs-3'),
            ),                
            Div(    
                #Div('preferred_site', css_class='col-xs-12'),
                #css_class="row"),
            ),
            Div(
                Field('bio'),
                css_class="row"),
            Submit('update', 'Aggiorna', css_class="btn-success"),
        )
        self.helper["association"].wrap(Field, HTML(
            "<p>Se pensi che la tua associazione di riferimento non sia tra le elencate ma debba esserlo, contatta <a href='https://savetheprince.net/contribute/' target='_blank'>uno dei responsabili del sito</a>!"))
        if self.instance.association:
            if self.instance.association.modello_liberatoria:
                if self.instance.association.modello_liberatoria.url:
                    self.helper["liberatoria"].wrap(Field, HTML(
                        "Scarica <a href='{}' target='_blank' >qua</a> il modello di liberatoria da compilare!".format(self.instance.association.modello_liberatoria.url)))
                else:
                    self.helper["liberatoria"].wrap(Field, HTML(
                        "Contatta la tua associazione di riferimento per ottenere il modello di liberatoria da compilare!"))
            else:
                self.helper["liberatoria"].wrap(Field, HTML(
                    "Contatta la tua associazione di riferimento per ottenere il modello di liberatoria da compilare!"))
        else:
            self.helper["liberatoria"].wrap(Field, HTML(
                "Seleziona una associazione, salva e rivisita questa pagina per ottenere il modello di liberatoria corrispondente da compilare"))

    class Meta:
        model = models.Profile
        fields = ['picture', 'phone_number', 'association',
                  'province', 'bio', 'profile_show', 'phone_show','mail_show', 'update_mail_receive','liberatoria']
