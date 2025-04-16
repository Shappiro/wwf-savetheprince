from django.views import generic
from django.shortcuts import render

from django.contrib.auth import get_user_model

from profiles.models import Profile, Association
from observations.models import Specie, Site, SiteImage, JournalImage, SiteDoc

from django.db.models import F, Func, Value
from django.db.models.functions import Lower

from utils.models import FAQModel

class HomePage(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, *args, **kwargs):
        context = super(HomePage, self).get_context_data(*args, **kwargs)
        context['associations'] = Association.objects.annotate(
            name_lower=Func(Func(Func(
                Lower(F('name')),
                Value(' '),
                Value('_'),
                function='replace'),Value('('),Value('_'),function="replace"),Value('('),Value('_'),function="replace")
        )
        return context


class AboutPage(generic.TemplateView):
    template_name = "about.html"

    def get_context_data(self, *args, **kwargs):
        context = super(AboutPage, self).get_context_data(*args, **kwargs)
        context['admins'] = Profile.objects.filter(
            user__is_staff=True, role__in=['admin', 'reference-site', 'reference-organization']).exclude(association_verified=False, profile_show=False).annotate(
            name_lower=Func(
                Lower(F('user__name')),
                Value(' '),
                Value('_'),
                function='replace')
        ).order_by('province','user__name')
        context['volunteers'] = Profile.objects.filter(
            user__is_staff=True, role='volunteer').exclude(association_verified=False, profile_show=False).annotate(
            name_lower=Func(
                Lower(F('user__name')),
                Value(' '),
                Value('_'),
                function='replace')
        ).order_by('user__name')
        context['associations'] = Association.objects.all().annotate(
            name_lower=Func(Func(Func(
                Lower(F('name')),
                Value(' '),
                Value('_'),
                function='replace'),Value('('),Value('_'),function="replace"),Value(')'),Value('_'),function="replace")
        ).order_by('name')
        # context['beasts'] = Specie.objects.all().annotate(
        #    name_lower=Func(
        #        Lower(F('vernacular_it')),
        #        Value(' '),
        #        Value('_'),
        #        function='replace')
        # ).order_by('vernacular_it')
        return context


class FriendsPage(generic.TemplateView):
    template_name = "friends.html"

    def get_context_data(self, *args, **kwargs):
        context = super(FriendsPage, self).get_context_data(*args, **kwargs)
        context['beasts'] = Specie.objects.all().annotate(
            name_lower=Func(
                Lower(F('vernacular_it')),
                Value(' '),
                Value('_'),
                function='replace')
        ).order_by('vernacular_it')
        return context


class JournalsPage(generic.TemplateView):
    template_name = "gallery_journals.html"

    def get_context_data(self, *args, **kwargs):
        context = super(JournalsPage, self).get_context_data(*args, **kwargs)
        context['journals'] = JournalImage.objects.all()
        return context

class FAQPage(generic.TemplateView):
    template_name = "faq.html"

    def get_context_data(self, *args, **kwargs):
        context = super(FAQPage, self).get_context_data(*args, **kwargs)
        context['faqs'] = FAQModel.objects.all()
        return context

class SitesPage(generic.TemplateView):
    template_name = "sites.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SitesPage, self).get_context_data(*args, **kwargs)
        provinces = list(Site.objects.values_list(
            'provincia', flat=True).distinct().order_by('provincia'))
        sitesobj = Site.objects.all()
        if not self.request.user.is_superuser:
            sitesobj = sitesobj.filter(attivo=True)
        context['ordered_sites'] = [
            {"province": province,
                "sites": [
                    {"name": site.name, 
                     "widget": site.meteoblue_widget,"flyer_url": site.flyer.url if site.flyer else None, "regione": site.regione, "descrizione": site.descrizione, "name_lower": site.name_lower,
                     "images":
                        [
                            {
                                "url": image.image.url,
                                "date": image.date,
                                "author": image.author,
                                "typeimg": image.typeimg,
                            } for image in SiteImage.objects.filter(site=site)
                        ],
                     "files":
                        [
                            {
                                "url": file.doc.url,
                                "title": file.title,
                                "doctype": file.doctype,
                                "author": file.author,
                                "date": file.date,

                            } for file in SiteDoc.objects.filter(site=site)
                        ]
                     } for site in sitesobj.filter(provincia=province)#.annotate(
                    #    name_lower=Func(
                    #        Lower(F('name')),
                    #        Value(' '),
                    #        Value('_'),
                    #        function='replace')
                    #)
                ]
             } for province in provinces
        ]
        return context


class ProjectPage(generic.TemplateView):
    template_name = "project.html"


class DataPage(generic.TemplateView):
    template_name = "data.html"

class ContactsPage(generic.TemplateView):
    template_name = "contacts.html"

class ContributePage(generic.TemplateView):
    template_name = "contribute.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ContributePage, self).get_context_data(*args, **kwargs)
        context['admins'] = Profile.objects.filter(
            user__is_staff=True, role__in=['admin', 'reference-site', 'reference-organization']).exclude(association_verified=False).annotate(
            name_lower=Func(
                Lower(F('user__name')),
                Value(' '),
                Value('_'),
                function='replace')
        ).order_by('province','user__name')
        context['associations'] = Association.objects.all()
        return context


class ManualPage(generic.TemplateView):
    template_name = "manual.html"


class BibliographyPage(generic.TemplateView):
    template_name = "biblio.html"

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def server_error_view(request):
    return render(request, '500.html', status=500)

def unauthorized_view(request, exception):
    return render(request, '403.html', status=403)