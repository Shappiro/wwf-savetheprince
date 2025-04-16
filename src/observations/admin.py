from django import forms

from django.db.models import Manager, Q
from django.contrib.gis import admin

from leaflet.admin import LeafletGeoAdminMixin
from sorl.thumbnail.admin import AdminImageMixin
from ajax_select.fields import AutoCompleteSelectMultipleField
from ajax_select.admin import AjaxSelectAdmin
from crum import get_current_user
from dal import autocomplete

from utils.views import send_email
from utils.functions import get_or_null

from django.urls import reverse

from profiles.models import Profile
from wwf_prince.utils import *

from .models import (Observation, Session, Site, SiteImage, Specie, SpecieImage, ObservationDetail, JournalImage, SiteDoc, SpecieDoc, YearlyReport, YearlyReportImage, SessionImage,SiteVolunteers, ObservationDetailImage, Pond, PondMonitor, PondImages)


class SpecieImageInline(AdminImageMixin, admin.TabularInline):
    model = SpecieImage
    extra = 0


class SpecieDocInline(AdminImageMixin, admin.TabularInline):
    model = SpecieDoc
    extra = 0

@admin.register(Specie)
class SpecieAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'immagine',)
    # list_editable = ('iucn',)
    readonly_fields = ('immagine',)

    inlines = [SpecieImageInline, SpecieDocInline, ]


@admin.register(JournalImage)
class JournalImageAdmin(admin.ModelAdmin):
    pass


class SiteImageInline(AdminImageMixin, admin.TabularInline):
    model = SiteImage
    extra = 0


class SiteDocInline(admin.TabularInline):
    model = SiteDoc
    extra = 0


class SiteManager(Manager):
    def get_queryset(self, request):
        if request.user.is_superuser:
            return Site.objects.all()
        else:
            return Site.objects.filter(attivo=True)


@admin.register(Site)
class SiteAdmin(LeafletGeoAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'attivo', 'provincia','comune', 'immagine',)
    readonly_fields = ['immagine','modified_by','created_by','modified','created','lunghezza']
    search_fields = ('name',)
    list_filter = ('attivo', 'regione','provincia',)
    ordering = ('name',)
    inlines = [SiteImageInline, SiteDocInline, ]

    fieldsets = (
        ('Campi automatici', {
            'fields': (
                ('created_by','modified_by',),
                ('created','modified',),
                ('lunghezza',),
            ),
            'classes': ('collapse','collapsed',),
        }),
        ('',{
            'fields':
                ('name','attivo',)
        }),
        ('Localizzazione', {
            'fields': (
                ('regione','provincia','comune',),
                #('regione_id','provincia_id','comune_id',),
                'geom',
            ),
        }),
        ('Caratteristiche',{
            'fields': (
                ('descrizione','meteoblue_widget'),
                ('flyer',),
            )
        })
    )

class SiteVolunteersForm(forms.ModelForm):
    sites = AutoCompleteSelectMultipleField('sites', label="Siti",help_text="Inizia a digitare un nome", required=False)
    class Meta:
        model = SiteVolunteers
        fields = ['sites']


@admin.register(SiteVolunteers)
class SiteVolunteersAdmin(AjaxSelectAdmin):
    list_display = ('__str__',)
    readonly_fields = ('id',)
    form = SiteVolunteersForm
    autocomplete_fields = ['profile']
    fieldsets = (
        (None, {
            'fields': (
                'profile','sites',
            ),
        }),
    )
class ObservationDetailAdminInline(admin.StackedInline):
    fieldsets = (
        ('Specie', {
            'fields': (
                'specie',
            ),
        }),
        ('Andata', {
            'classes': ('collapse', 'collapsed', 'speciedetail',),
            'fields': (
                'alive_female_andata',
                'alive_male_andata',
                'alive_indet_andata',
            ),
        }),
        ('Ritorno', {
            'classes': ('collapse', 'collapsed', 'speciedetail',),
            'fields': (
                'alive_female_ritorno',
                'alive_male_ritorno',
                'alive_indet_ritorno',
            ),
        }),
        ('Morti', {
            'classes': ('collapse', 'collapsed', 'speciedetail',),
            'fields': (
                'dead_female',
                'dead_male',
                'dead_indet',
            ),
        }),
        ('Direzione indeterminata', {
            'classes': ('collapse', 'collapsed', 'speciedetail',),
            'fields': (
                'alive_female_indet',
                'alive_male_indet',
                'alive_indet_indet',
            ),
        }),
        ('Altro (giovani e neometamorfosati)', {
            'classes': ('collapse', 'collapsed', 'speciedetail',),
            'fields': (
                ('giovani'),
                ('neometamorfosati_vivi_stima','neometamorfosati_morti_stima',),
                ('neometamorfosati_vivi','neometamorfosati_morti',),
            ),
        }),
        ('Sospetti malati', {
            'classes': ('collapse', 'collapsed', 'speciedetail',),
            'fields': (
                ('malati'),
                ('malati_descrizione',),
                ('malati_analisi','malati_analisi_invio',),
                ('malati_conferma',),
            ),
        }),                
    )

    model = ObservationDetail
    extra = 0
    ordering = ("specie__specie",)


class ObservationAdminInline(admin.StackedInline):
    fielsets = (
        (None, {
            'fields': (
                ('specie', 'n',),
                ('sex', 'state',),
                'direction',
                'life',
            )
        }),
    )

    model = Observation
    extra = 0

class SessionForm(forms.ModelForm):

    begin = forms.TimeField(label="Ora inizio", widget=forms.TimeInput(
        format='%H:%M', attrs={'class': 'timepicker'}), initial='00:00', input_formats=["%H:%M"])
    end = forms.TimeField(label="Ora fine", widget=forms.TimeInput(
        format='%H:%M', attrs={'class': 'timepicker'}), initial='00:00', input_formats=["%H:%M"])
    
    #volontari = AutoCompleteSelectMultipleField('profiles', label="Volontari registrati",help_text="Inizia a digitare un nome", required=False)

    volontari = forms.ModelMultipleChoiceField(
        queryset = Profile.objects.all(),required=False,
        widget = autocomplete.ModelSelect2Multiple(url='profile-autocomplete')
    )
    site = forms.ModelChoiceField(
        queryset = Site.objects.all(),required=True,
        widget = autocomplete.ModelSelect2(url='site-autocomplete'),label='Sito'
    )
    
    class Meta:
        model = Profile
        fields = ['volontari','site']

    # Precompilo il sito preferito del volontario
    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)
        user = get_current_user()
        initial_site_pk = Profile.objects.filter(
            user=user).values_list('preferred_site')[0][0]
        if initial_site_pk:
            self.fields['site'] = forms.ModelChoiceField(
            queryset = Site.objects.all(),required=True,
            widget = autocomplete.ModelSelect2(url='site-autocomplete'),initial=initial_site_pk,label='Sito'
        )
class SessionImageInline(AdminImageMixin, admin.TabularInline):
    model = SessionImage
    extra = 0
    
@admin.register(Session)
class SessionAdmin(AjaxSelectAdmin):
    #autocomplete_fields = ['users']
    list_display = ('site', 'date', 'begin', 'end','created_by',)
    readonly_fields = ['created_by', 'modified_by','created','modified']
    autocomplete_fields = ['site']
    fieldsets = (
        ('Campi automatici', {
            'fields': (
                ('created_by','modified_by',),
                ('created','modified',),
            ),
            'classes': ('collapse','collapsed',),
        }),
        ('Dettagli sessione', {
            'fields': (
                'site',
                ('date','ended_next_day',),
                ('begin', 'end',),
                ('meteo', 'vento',),
                ('temperature',),
                ('volontari',),
                ('volontari_unregistered',),
            )
        }),
        ('Note', {
            'classes': ('collapse', 'closed'),
            'fields': (
                'note',
            ),
        }),
    )
    search_fields = ('site__name',)
    list_filter = ('site', 'date',)
    order = ('date',)
    # VolontariInline, ]
    inlines = [ObservationDetailAdminInline, SessionImageInline,]
    form = SessionForm

    class Media:
        css = {
            "all": (
                "css/admin/timepicker-init.css",
                "css/admin/modifier.css",
            )
        }
        js = (
            #'js/admin/collapse.js',
            #'https://code.jquery.com/jquery-3.6.3.min.js',
            #'https://code.jquery.com/jquery-migrate-3.4.0.min.js',
            'js/admin/jquery-clock-timepicker.min.js',
            'js/admin/timepicker-init.js',
            'js/admin/all.js',
        )

    # Rimuovo i dash dalla lista di azioni
    def get_action_choices(self, request):
        choices = super(SessionAdmin, self).get_action_choices(request)
        # choices is a list, just change it.
        # the first is the BLANK_CHOICE_DASH
        choices.pop(0)
        return choices

    def get_queryset(self, request):
        query = super().get_queryset(request)
        
        # superutente: vede tutto
        if request.user.is_superuser:
            return query

        # referente organizzazione: vede tutte le sessioni create o modificate da qualche utente entro la sua organizzazione        
        if request.user.profile.role == 'reference-organization':
            return query.filter(created_by__profile__association=request.user.profile.association) | query.filter(modified_by__profile__association=request.user.profile.association)

        # volontario: vede il suo sito, e i siti ai quali è associato se ne ha
        else:
            # recupero sito/siti
            sites = [request.user.profile.preferred_site.id]            
            volsites = SiteVolunteers.objects.filter(profile=request.user.profile)
            if volsites:
                sites = sites + list(volsites.values_list('sites__id',flat=True))

            # se il volontario è un referente di sito, per quei siti ai quali è associato vede tutti i dati
            if request.user.profile.role == 'reference-site':
                return query.filter(site__in=sites)
            else:
                # altrimenti, vede solo i dati dei siti modificati / creati da lui
                return query.filter(Q(site__in=sites) | Q(created_by=request.user) | Q(modified_by=request.user))

    def save_model(self, request, obj, form, change):
        #form.cleaned_data['volontari'] = Profile.objects.filter(pk__in=dict(request.POST).get('volontari'))
        #obj.effort = obj.eff
        super().save_model(request, obj, form, change)
        
    def save_related(self, request, form, formsets, change):
        # prima salvo il modello, poi salvo i vari formset che vi dipendono, quindi mando la mail
        super().save_related(request, form, formsets, change)
        #super().save_model(request, form.instance, form, change)        
        #form.save_m2m()
        #for formset in formsets:
        #    self.save_formset(request, form, formset, change=change)
        # Per i dettagli delle specie
        obj = form.instance
        obs = obj.observationdetail_session.all()
        excluded_fields = ['id','specie','session','created_by','modified_by','created','modified']
        fields_tocheck = [
            f.name for f in ObservationDetail._meta.get_fields()
            if (
                f.name not in excluded_fields
                and not (f.is_relation and f.related_model == ObservationDetailImage)
            )
        ]
        fields_tocheck_verbose = [
            f.verbose_name for f in ObservationDetail._meta.get_fields()
            if (
                hasattr(f, 'verbose_name')
                and f.name not in excluded_fields
                and not (f.is_relation and f.related_model == ObservationDetailImage)
            )
        ]
        subject = 'Save the Prince | {} ({}) - nuovo inserimento sessione'.format(
            get_or_null(obj.site.name),
            get_or_null(obj.site.provincia),
        )
        message = """<strong>Messaggio automatico</strong><br>
            <strong>Inserimento nuova sessione per sito {} ({}) in portale Save the Prince!</strong>
            <br>
            <br>
            <h4>Dati di dettaglio della sessione</h4><hr>
            <strong>Utente</strong>: {} ({})<br>
            <strong>Sito</strong>:{}<br>
            <strong>Data</strong>: {}<br>
            <strong>Ora inizio</strong>: {}<br>
            <strong>Ora fine</strong>: {}<br>
            <strong>Meteo</strong>: {}<br>
            <strong>Vento</strong>: {}<br>
            <strong>Temperatura</strong>: {}<br>
            
        """.format(
            get_or_null(obj.site.name),get_or_null(obj.site.provincia),
            get_or_null(obj.modified_by.name),get_or_null(obj.modified_by.email),
            get_or_null(obj.site.name),
            get_or_null(obj.date),get_or_null(obj.begin),get_or_null(obj.end),
            get_or_null(obj.meteo),get_or_null(obj.vento),get_or_null(obj.temperature)
        )
        if obs is not None:
            message = message + "<h4>Riassunto osservazioni</h4><hr>"
            for specie in obs:
                message = message + "<strong><em>{}</em></strong><br>".format(specie.specie)
                for field in fields_tocheck:
                    if getattr(specie,field) not in [None,'']:
                        message = message + "{}: <strong>{}</strong><br>".format(fields_tocheck_verbose[fields_tocheck.index(field)],getattr(specie,field))
        message = message + "<br><a href='https://savetheprince.net/admin/observations/session/" + str(get_or_null(obj.pk)) + "/change'>Modifica sessione</a><br>"
        message = message + """
            <br>
            <br>
            <em><a href="https://savetheprince.net">Progetto Save the Prince</a></em>
            <br>
            <br>
            <image src="https://savetheprince.net/media/loghi/orizzontale/logo_orizzontale_nero.png" width=200></image><br>
        """
        send_email("salvataggioanfibi@gmail.com", "salvataggioanfibi@gmail.com",subject, str(message), message)
        if obj.modified_by.profile.update_mail_receive:
            send_email("salvataggioanfibi@gmail.com", obj.modified_by.email, subject, str(message), message)


class YearlyReportImageInline(AdminImageMixin, admin.TabularInline):
    model = YearlyReportImage
    extra = 0

class YearlyReportForm(forms.ModelForm):
    class Meta:
        model = YearlyReport
        fields = ['site', ]

    # Precompilo il sito preferito del volontario
    #def __init__(self, *args, **kwargs):
    #    super(YearlyReportForm, self).__init__(*args, **kwargs)
    #    user = get_current_user()
    #    initial_site_pk = Profile.objects.filter(
    #        user=user).values_list('preferred_site')[0][0]
    #    if initial_site_pk:
    #        self.fields['site'] = forms.ModelChoiceField(queryset=Site.objects.all(), # label="Sito",initial=initial_site_pk)

@admin.register(YearlyReport)
class YearlyReportAdmin(admin.ModelAdmin):
    list_display = ('site', 'year','date_begin', 'date_end')
    readonly_fields = ['created_by', 'modified_by','created','modified','n_volontari','n_uscite']
    autocomplete_fields = ['site']
    list_filter = ('year', 'site',)

    inlines = [ YearlyReportImageInline ]
    form = YearlyReportForm
    fieldsets = (
        ('Campi automatici', {
            'fields': (
                ('created_by','modified_by',),
                ('created','modified',),
                ('n_volontari','n_uscite',),
            ),
            'classes': ('collapse','collapsed',),
        }),
        ('Dettagli generali', {
            'fields': (
                ('site','year',),
                ('date_begin', 'date_end',),
                ('date_barriers_begin', 'date_barriers_end',),
            )
        }),
        ('Note', {
            #'classes': ('collapse',),
            'fields': (
                'note_riservate',
                'andamento',
                'note_sito',
                'note_traffico',
                'note_fauna',
                'note_altro',
            ),
        }),
        ('Altro',{
            'classes': ('collapse','closed'),
            'fields': ('specie_toexclude',),
        })        
    )

    def view_on_site(self, obj):
        path = reverse('yearlyreport-detail', kwargs={'pk': obj.pk})
        url_complete = 'https://{domain}{path}'.format(domain='savetheprince.net', path=path)
        return url_complete
    
    # def get_other_images(self,obj):

class PondImagesInline(AdminImageMixin, admin.TabularInline):
    model = PondImages
    extra = 0

@admin.register(Pond)
class PondAdmin(LeafletGeoAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'regione', 'provincia', 'comune', 'attivo', 'tutelato')
    readonly_fields = ['immagine']
    search_fields = ('name', 'regione', 'provincia', 'comune')
    list_filter = ('attivo', 'tutelato', 'regione', 'provincia')
    ordering = ('name',)
    inlines = [PondImagesInline]

    fieldsets = (
        ('Informazioni generali', {
            'fields': (
                'name', 'regione', 'provincia', 'comune', 'descrizione', 'attivo', 'tutelato',
            ),
        }),
        ('Localizzazione', {
            'fields': (
                'geom', 'lunghezza', 'data_scoperta',
            ),
        }),
        ('Specie e contatti', {
            'fields': (
                'species', 'proprietario', 'contatto_proprietario',
            ),
        }),
        ('Immagine rappresentativa', {
            'fields': ('immagine',),
        }),
    )

@admin.register(PondMonitor)
class PondMonitorAdmin(admin.ModelAdmin):
    list_display = ('pond', 'date', 'time', 'end', 'meteo', 'vento', 'temperature')
    search_fields = ('pond__name', 'date')
    list_filter = ('pond', 'date', 'meteo', 'vento')
    ordering = ('-date', '-time', 'pond')

    fieldsets = (
        ('Informazioni generali', {
            'fields': (
                'pond', 'date', 'time', 'end', 'meteo', 'vento', 'temperature',
            ),
        }),
        ('Volontari', {
            'fields': (
                'volontari', 'volontari_unregistered',
            ),
        }),
        ('Specie osservate e note', {
            'fields': (
                'species', 'note',
            ),
        }),
    )

@admin.register(PondImages)
class PondImagesAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('pond', 'image', 'author')
    search_fields = ('pond__name', 'author')
    list_filter = ('pond',)
    ordering = ('pond',)

    fieldsets = (
        ('Informazioni immagine', {
            'fields': (
                'pond', 'image', 'descr', 'author',
            ),
        }),
    )