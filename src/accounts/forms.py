from __future__ import unicode_literals
from django.template import loader
from authtools import forms as authtoolsforms
from django.contrib.auth.forms import PasswordResetForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Layout, Submit
from django import forms
from dal import autocomplete
from django.contrib.auth import forms as authforms
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django_filters.fields import ModelChoiceField

from profiles.models import Profile, Association
from observations.models import Site
from utils.views import send_email

from localflavor.it.forms import ITRegionProvinceSelect
#from localflavor.it_region import REGION_CHOICES, REGION_PROVINCE_CHOICES
from wwf_prince.utils import PROVINCIA_CHOICES
#PROVINCIA_CHOICES.insert(0, ('', '-------'))

class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(label="Ricordami",required=False, initial=False)
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            api_params={'hl': 'it'}
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["username"].widget.input_type = "email"  # ugly hack

        self.helper.layout = Layout(
            Field('username', placeholder="Inserisci mail", autofocus=""),
            Field('password', placeholder="Inserisci password"),
            Field("captcha"),            
            HTML('<a href="{}">Password dimenticata?</a>'.format(
                reverse("accounts:password-reset"))),
            Field('remember_me'),
            Submit('sign_in', 'Entra',
                   css_class="btn btn-lg btn-primary btn-block"),
        )


def get_provinces_list():
    return [a[0] for a in PROVINCIA_CHOICES]

class SignupForm(authtoolsforms.UserCreationForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            api_params={'hl': 'it'}
        )
    )
    profile_name = forms.CharField(label="Nome",max_length=400)
    profile_surname = forms.CharField(label="Cognome",max_length=400)

    association = forms.ModelChoiceField(queryset=Association.objects.all().order_by('name'))
    site = forms.ModelChoiceField(queryset=Site.objects.all().order_by('name'))#,widget=autocomplete.ModelSelect2(url='site-autocomplete'))

    #province = #ITRegionProvinceSelect()
    
    province = forms.ChoiceField(
        choices=PROVINCIA_CHOICES,
        #widget=autocomplete.ListSelect2(url='provinces-autocomplete')
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["email"].widget.input_type = "email"  # ugly hack
        self.fields['name'].required = False
        self.fields['association'].label = "Associazione di riferimento"
        self.fields['site'].label = "Sito di salvataggio preferito"
        self.fields['province'].label = "Provincia di riferimento"

        self.helper.layout = Layout(
            Field('email', placeholder="Inserisci mail", autofocus=""),
            Field('name', css_class="hideform"),
            Field('profile_name', placeholder="Inserisci il tuo nome"),
            Field('profile_surname', placeholder="Inserisci il tuo cognome"),
            Field('association', placeholder="Associazione di riferimento"),
            Field('province', placeholder="Provincia di riferimento"),
            Field('site',placeholder="Sito di salvataggio preferito"),
            Field('password1', placeholder="Inserisci password"),
            Field('password2', placeholder="Reinserisci la password"),
            Field("captcha"),
            #Field('province', placeholder="Regione di azione"),
            Submit('sign_up', 'Registrati', css_class="btn-warning"),
        )

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.name = self.cleaned_data['profile_name'] + ' ' + self.cleaned_data['profile_surname']
        user.save()
        user_profile = Profile(user=user,profile_name=self.cleaned_data['profile_name'],profile_surname=self.cleaned_data['profile_surname'],association=self.cleaned_data['association'],preferred_site=self.cleaned_data['site'])
        user_profile.save()
        return user

class PasswordChangeForm(authforms.PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field('old_password', placeholder="Inserisci la vecchia password",
                  autofocus=""),
            Field('new_password1', placeholder="Inserisci la nupva password"),
            Field('new_password2',
                  placeholder="Inserisci la nuova password (di nuovo)"),
            Submit('pass_change', 'Cambia password', css_class="btn-warning"),
        )


class PasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('email', placeholder="Inserisci email",
                  autofocus=""),
            Submit('pass_reset', 'Reset password', css_class="btn-warning"),
        )

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email` using
        `anymail.backends.postmark.EmailBackend`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)
        send_email('salvataggioanfibi@gmail.com', to_email, subject, body, body)

class SetPasswordForm(authforms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field('new_password1', placeholder="Inserisci la nuova password",
                  autofocus=""),
            Field('new_password2',
                  placeholder="Inserisci la nuova password (di nuovo)"),
            Submit('pass_change', 'Cambia password', css_class="btn-warning"),
        )
        
