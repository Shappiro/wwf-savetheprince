from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render
from dal import autocomplete
from django.views.generic.detail import DetailView

import datetime
import pandas as pd

from django.db.models import F, Func, Value, Sum
from django.db.models.functions import Lower

from .models import Site, SiteSummary, Specie, Observation
from .forms import SiteForm

from rest_framework import filters, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend


from .serializers import SiteSerializer, ObservationSerializer, SiteSummarySerializer
from django.db.models import Q, F

app_name = __package__

from rest_framework.settings import api_settings
from rest_framework_csv import renderers as r
from observations.models import Session, YearlyReport
from profiles.models import Profile

class DataPage(generic.TemplateView):
    template_name = app_name + "/data.html"

    def get_context_data(self, **kwargs):
        context = super(DataPage, self).get_context_data(**kwargs)
        context['sites'] = Site.objects.filter(attivo=True).order_by('name')
        context['regions'] = Site.objects.filter(attivo=True).values_list(
            'regione', flat=True).distinct().order_by('regione')
        context['provinces'] = Site.objects.filter(attivo=True,provincia__isnull=False).values_list(
            'provincia', flat=True).distinct().order_by('provincia')
        context['sitenames'] = Site.objects.filter(attivo=True).values_list(
            'name', flat=True).distinct().order_by('name')
    
        return context


@login_required
def site_new(request):
    if request.method == 'POST':
        # I may want to add some precompiled fields to the form:
        # I therefore have to pass an instance of the model to the form
        # site = Site(user=request.user) # gets the compiling user
        form = SiteForm(data=request.POST  # ,instance=site
                        )
        if form.isvalid():
            form.save()
            return redirect(app_name + "/data.html")
    else:  # if user is coming to insert data in the form, send it to the correct template
        form = SiteForm()  # Initialize an empty form
    return render(request, app_name + "/new_site.html", {"form": form})


def site_species(request):
    site = request.GET.get('site')
    return render(request, app_name + '/site_species.html', {
        'sitespecies_info': Specie.objects.filter(id__in=list(Observation.objects.filter(session__site__name=site).values_list('specie', flat=True).distinct()))
    })


class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SiteSerializer
    queryset = Site.objects.all().order_by('name')
    #filter_class = SiteFilter
    filter_backends = [DjangoFilterBackend]    
    filterset_fields = ['name', 'regione', 'provincia']

    def paginate_queryset(self, queryset, view=None):
        if 'no_page' in self.request.query_params:
            return None
        else:
            return self.paginator.paginate_queryset(queryset, self.request, view=self)  

class SiteSummaryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SiteSummarySerializer
    queryset = SiteSummary.objects.all().order_by('name')
    filter_backends = [DjangoFilterBackend]    
    filterset_fields = ['name', 'year', 'specie']
    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.PaginatedCSVRenderer, )

    def paginate_queryset(self, queryset, view=None):
        if 'no_page' in self.request.query_params:
            return None
        else:
            return self.paginator.paginate_queryset(queryset, self.request, view=self)     


class ObservationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ObservationSerializer
    queryset = Observation.objects.all()
    search_fields = ['specie__specie', 'session__site__name']
    filter_backends = [filters.SearchFilter]    
    filterset_fields = ['site_name', 'specie_name']
    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.PaginatedCSVRenderer, )

    def paginate_queryset(self, queryset, view=None):
        if 'no_page' in self.request.query_params:
            return None
        else:
            return self.paginator.paginate_queryset(queryset, self.request, view=self)   

# CHARTS
class GraphPage(generic.TemplateView):
    template_name = app_name + "/graphs.html"

    def get_context_data(self, **kwargs):
        context = super(GraphPage, self).get_context_data(**kwargs)
        context['sitenames'] = Site.objects.filter(attivo=True).annotate(n=Sum('sites__observations__n')).values('n','name').filter(n__gt=1).values('name').order_by('name')
        context['species'] = Observation.objects.values('specie__specie').annotate(
            num=Sum('n'),
            name_lower=Func(
                    Func(
                        Lower(F('specie__specie')),
                        Value(' '),
                        Value('_'),
                    function='replace'),
                Value('.'),
                Value(''),
            function='replace')
        ).filter(num__gt=10).order_by('-num')
        return context

class YearlyReportDetail(LoginRequiredMixin,DetailView):
    model = YearlyReport
    template_name = 'observations/yearly_report.html'
    context_object_name = 'report'

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        get_data = request.query_params

        data = []
        species = []
        queryset = SiteSummary.objects.all().order_by('name')
        years = list(set(queryset.values_list('year', flat=True)))
        years.sort()

        if get_data.get('site', None) and get_data.get('year', None) and get_data.get('specie', None):
            site = get_data.get('site')
            year = get_data.get('year')
            specie = get_data.get('specie', None)
            queryset = queryset.filter(name=site,year=year)
            #q = Session.objects.filter(site__name=get_data.get('site'),date__year=get_data.get('site'))
            #species = list(set([item for sublist in [list(s.observations.values_list('specie__specie',flat=True).distinct()) for s in q] for item in sublist]))
            species = list(set(queryset.values_list('specie',flat=True)))
            species.sort()
            
            queryset = Observation.objects.filter(session__site__name=site,session__date__year=year).values('session__date','specie__specie','direction','life').annotate(n=Sum('n'))

            date_begin = min(queryset.values_list('session__date',flat=True))
            date_end = max(queryset.values_list('session__date',flat=True))
            dates = [date_begin + datetime.timedelta(days=x) for x in range(0, (date_end-date_begin).days+1)]            

            dates = pd.DataFrame(dates,columns=['session__date'])
            res = pd.DataFrame.from_dict(queryset)
            dates = dates.merge(res,on='session__date',how='left').sort_values(by=['session__date'])

            #for specie in species:
            #spec = dates[dates["specie__specie"] == specie]
            if specie in species:
                data.append({
                    "specie": specie,
                    "labels": [d.strftime("%d-%m") for d in list(dates["session__date"])],
                    "datasets": [{
                        "label": 'Andata',
                        "maxBarThickness": 50,
                        "backgroundColor": "blue",
                        "data": list(dates["n"].where((dates["specie__specie"] == specie) & (dates["direction"] == 'AND'), 0))
                    }, {
                        "label": 'Ritorno',
                        "maxBarThickness": 50,
                        "backgroundColor": "orange",
                        "data": list(dates["n"].where((dates["specie__specie"] == specie) & (dates["direction"] == 'RIT'), 0))
                    },{
                        "label": 'Indeterminati',
                        "maxBarThickness": 50,
                        "backgroundColor": "red",
                        "data": list(dates["n"].where((dates["specie__specie"] == specie) & (dates["direction"] == 'IND'), 0))
                    }]
                })
            return Response(data)


        ### andata e ritorno nel tempo per specie, per un certo anno
        if get_data.get('site', None) and get_data.get('year', None):
            site = get_data.get('site')
            year = get_data.get('year')
            queryset = queryset.filter(name=site,year=year)
            #q = Session.objects.filter(site__name=get_data.get('site'),date__year=get_data.get('site'))
            #species = list(set([item for sublist in [list(s.observations.values_list('specie__specie',flat=True).distinct()) for s in q] for item in sublist]))
            species = list(set(queryset.values_list('specie',flat=True)))
            species.sort()
            
            queryset = Observation.objects.filter(session__site__name=site,session__date__year=year).values('session__date','specie__specie','direction','life').annotate(n=Sum('n'))

            date_begin = min(queryset.values_list('session__date',flat=True))
            date_end = max(queryset.values_list('session__date',flat=True))
            dates = [date_begin + datetime.timedelta(days=x) for x in range(0, (date_end-date_begin).days+1)]            

            dates = pd.DataFrame(dates,columns=['session__date'])
            res = pd.DataFrame.from_dict(queryset)
            dates = dates.merge(res,on='session__date',how='left').sort_values(by=['session__date'])

            for specie in species:
                #spec = dates[dates["specie__specie"] == specie]
                data.append({
                    "specie": specie,
                    "labels": [d.strftime("%d-%m") for d in list(dates["session__date"])],
                    "datasets": [{
                        "label": 'Andata',
                        "maxBarThickness": 50,
                        "backgroundColor": "blue",
                        "data": list(dates["n"].where((dates["specie__specie"] == specie) & (dates["direction"] == 'AND'), 0))
                    }, {
                        "label": 'Ritorno',
                        "maxBarThickness": 50,
                        "backgroundColor": "orange",
                        "data": list(dates["n"].where((dates["specie__specie"] == specie) & (dates["direction"] == 'RIT'), 0))
                    },{
                        "label": 'Indeterminati',
                        "maxBarThickness": 50,
                        "backgroundColor": "orange",
                        "data": list(dates["n"].where((dates["specie__specie"] == specie) & (dates["direction"] == 'IND'), 0))
                    }]
                })
            return Response(data)

        if get_data.get('site', None):
            queryset = queryset.filter(name=get_data.get('site'))
            species = list(set(queryset.values_list('specie', flat=True)))
            species.sort()

            for specie in species:
                labels = []
                dataspecie_alive = []
                dataspecie_dead = []

                specie_queryset = queryset.filter(specie=specie).order_by(
                    'year').values('year', 'specie', 'alive').annotate(n=Sum('n'))

                for year in years:
                    #for summary in specie_queryset:
                    labels.append(year)

                    alive = specie_queryset.filter(year=year,alive=True)
                    dead = specie_queryset.filter(year=year,alive=False)
                    if alive and dead:
                        dataspecie_alive.append(alive[0]["n"])
                        dataspecie_dead.append(dead[0]["n"])
                    elif alive and not dead: 
                        dataspecie_alive.append(alive[0]["n"])
                        dataspecie_dead.append(0)
                    elif dead and not alive:
                        dataspecie_alive.append(0)
                        dataspecie_dead.append(dead[0]["n"])                    
                    else:
                        dataspecie_alive.append(0)
                        dataspecie_dead.append(0)

                data.append({
                    "specie": specie,
                    "labels": labels,
                    "datasets": [{
                        "label": 'Vivi',
                        "maxBarThickness": 50,
                        "backgroundColor": "green",
                        "data": dataspecie_alive
                    }, {
                        "label": 'Morti',
                        "maxBarThickness": 50,
                        "backgroundColor": "red",
                        "data": dataspecie_dead
                    }]
                })

        elif get_data.get('specie', None):
            specie = get_data.get('specie')
            queryset_temp = queryset.filter(specie=specie).order_by(
                'year').values('year', 'alive').annotate(n=Sum('n'))
            # sites = queryset.values_list('name', flat=True).distinct()
            # for site in sites:
            labels = []
            dataspecie_alive = []
            dataspecie_dead = []

            # site_queryset = queryset_temp.filter(name=site).order_by(
            #        'year').values('year', 'alive').annotate(n = Sum('n'))

            # for summary in site_queryset:
            for year in years:
                #for summary in specie_queryset:
                labels.append(year)

                alive = queryset_temp.filter(year=year,alive=True)
                dead = queryset_temp.filter(year=year,alive=False)
                if alive and dead:
                    dataspecie_alive.append(alive[0]["n"])
                    dataspecie_dead.append(dead[0]["n"])
                elif alive and not dead: 
                    dataspecie_alive.append(alive[0]["n"])
                    dataspecie_dead.append(0)
                elif dead and not alive:
                    dataspecie_alive.append(0)
                    dataspecie_dead.append(dead[0]["n"])                    
                else:
                    dataspecie_alive.append(0)
                    dataspecie_dead.append(0)                


                data.append({
                    "specie": specie,
                    "labels": labels,
                    "datasets": [{
                        "label": 'Vivi',
                        "maxBarThickness": 50,
                        "backgroundColor": "green",
                        "data": dataspecie_alive
                    }, {
                        "label": 'Morti',
                        "maxBarThickness": 50,
                        "backgroundColor": "red",
                        "data": dataspecie_dead
                    }]
                })

        else:
            queryset = queryset.order_by('year').values('year', 'specie','alive').annotate(n=Sum('n'))
            species = list(set(queryset.values_list('specie', flat=True)))
            species.sort()

            for specie in species:
                labels = []
                dataspecie_alive = []
                dataspecie_dead = []

                specie_queryset = queryset.filter(specie=specie)

                for year in years:
                    #for summary in specie_queryset:
                    labels.append(year)

                    alive = specie_queryset.filter(year=year,alive=True)
                    dead = specie_queryset.filter(year=year,alive=False)
                    if alive and dead:
                        dataspecie_alive.append(alive[0]["n"])
                        dataspecie_dead.append(dead[0]["n"])
                    elif alive and not dead: 
                        dataspecie_alive.append(alive[0]["n"])
                        dataspecie_dead.append(0)
                    elif dead and not alive:
                        dataspecie_alive.append(0)
                        dataspecie_dead.append(dead[0]["n"])                    
                    else:
                        dataspecie_alive.append(0)
                        dataspecie_dead.append(0) 

                    data.append({
                        "specie": specie,
                        "labels": labels,
                        "datasets": [{
                            "label": 'Vivi',
                            "maxBarThickness": 50,
                            "backgroundColor": "green",
                            "data": dataspecie_alive
                        }, {
                            "label": 'Morti',
                            "maxBarThickness": 50,
                            "backgroundColor": "red",
                            "data": dataspecie_dead
                        }]
                    })

        return Response(data)

class SiteAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Site.objects.filter(attivo=True).order_by('name')
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class SiteAutoCompleteGrouped(autocomplete.Select2GroupListView):
    
    def get_list(self):
        qs = Site.objects.filter(attivo=True).order_by('name')
        provs = list(set([q.provincia for q  in qs]))
        grouped = []
        for prov in provs:
            grouped.append( (prov,list(qs.filter(provincia=prov).values_list('name',flat=True))) )
        return grouped

class ProfileAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Profile.objects.none()

        qs = Profile.objects.all()

        if self.q:
            qs = qs.filter(Q(profile_name__icontains=self.q) | Q(profile_surname__icontains=self.q) | Q(user__name__icontains=self.q))

        return qs

class ChartEffortData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        get_data = request.query_params

        data = []
        species = []
        queryset = SiteSummary.objects.all().order_by('name')
        years = list(set(queryset.values_list('year', flat=True)))
        years.sort()

        if get_data.get('site', None) and get_data.get('year', None):
            site = get_data.get('site')
            year = get_data.get('year')
            queryset = Session.objects.filter(site__name=site,date__year=year).values_list('date','effort')

            date_begin = min(queryset.values_list('date',flat=True))
            date_end = max(queryset.values_list('date',flat=True))
            dates = [date_begin + datetime.timedelta(days=x) for x in range(0, (date_end-date_begin).days+1)]            

            dates = pd.DataFrame(dates,columns=['date'])
            res = pd.DataFrame.from_dict(queryset)
            res.columns = ['date','effort']
            dates = dates.merge(res,on='date',how='left').sort_values(by=['date'])
            dates['effort'] = dates['effort'].fillna(0)
            dates = dates.groupby('date').sum()
            data.append({
                "labels": [d.strftime("%d-%m") for d in list(dates["date"])],
                "datasets": [{
                    "label": 'Sforzo',
                    "maxBarThickness": 50,
                    "backgroundColor": "blue",
                    "data": list(dates["effort"])
                }]
            })
            return Response(data)
        
        elif get_data.get('site', None) and get_data.get('date_begin', None) and get_data.get('date_end', None):
            site = get_data.get('site')
            date_begin = datetime.datetime.strptime(get_data.get('date_begin'),'%Y-%m-%d')
            date_end = datetime.datetime.strptime(get_data.get('date_end'),'%Y-%m-%d')
            queryset = Session.objects.filter(site__name=site,date__gte=date_begin,date__lte=date_end).values_list('date','effort')

            dates = [date_begin + datetime.timedelta(days=x) for x in range(0, (date_end-date_begin).days+1)]            

            dates = pd.DataFrame(dates,columns=['date'])
            res = pd.DataFrame.from_dict(queryset)
            res.columns = ['date','effort']
            res.date = res.date.astype('datetime64[ns]')
            
            dates = dates.merge(res,on='date',how='left').sort_values(by=['date'])
            dates['effort'] = dates['effort'].fillna(0)

            data.append({
                "labels": [d.strftime("%d-%m") for d in list(dates["date"])],
                "datasets": [{
                    "label": 'Sforzo',
                    "maxBarThickness": 50,
                    "backgroundColor": "blue",
                    "data": list(dates["effort"])
                }]
            })
            return Response(data)

        else:
            return None

class ChartYearlyDirectionSpecieData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        get_data = request.query_params

        data = []
        species = []

        queryset = SiteSummary.objects.filter(name=get_data.get('site'))
        years = list(set(queryset.values_list('year', flat=True)))
        years.sort()

        queryset = queryset.order_by('year').values('year', 'specie','direction','sex','alive','n')

        if get_data.get('specie',None):
            species = [get_data.get('specie')]
        else:
            species = list(set(queryset.values_list('specie', flat=True)))
            species.sort()
        for specie in species:
            specie_queryset = queryset.filter(specie=specie)
            if specie_queryset:
                labels = []
                dataspecie_direction_ind = []
                dataspecie_direction_and = []
                dataspecie_direction_rit = []

                for year in years:
                    labels.append(year)

                    direction_ind = specie_queryset.filter(year=year,alive=True,direction='IND')
                    direction_rit = specie_queryset.filter(year=year,alive=True,direction='RIT')
                    direction_and = specie_queryset.filter(year=year,alive=True,direction='AND')

                    #dataspecie_dead.append(dead[0]["n"]) if dead else dataspecie_dead.append(0)
                    dataspecie_direction_rit.append(direction_rit.aggregate(Sum('n'))["n__sum"]) if direction_rit else dataspecie_direction_rit.append(0)
                    dataspecie_direction_and.append(direction_and.aggregate(Sum('n'))["n__sum"]) if direction_and else dataspecie_direction_and.append(0)
                    dataspecie_direction_ind.append(direction_ind.aggregate(Sum('n'))["n__sum"]) if direction_ind else dataspecie_direction_ind.append(0)
                    
                if not all(v== 0 for v in dataspecie_direction_rit + dataspecie_direction_and + dataspecie_direction_ind):
                    data.append({
                        "specie": specie,
                        "labels": labels,
                        "datasets": [{
                            "label": 'Direzione indeterminata',
                            "maxBarThickness": 25,
                            "backgroundColor": "gray",
                            "data": dataspecie_direction_ind
                        }, {
                            "label": 'Andate',
                            "maxBarThickness": 25,
                            "backgroundColor": "blue",
                            "data": dataspecie_direction_and
                            
                        }, {
                            "label": 'Ritorni',
                            "maxBarThickness": 25,
                            "backgroundColor": "orange",
                            "data": dataspecie_direction_rit                        
                        }]
                    })

        return Response(data)

class ChartYearlyDeadAliveSpecieData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        get_data = request.query_params

        data = []
        labels = []
        specie = get_data.get('specie')
        queryset = SiteSummary.objects.filter(name=get_data.get('site'),specie=specie).values('year', 'specie','alive').annotate(n=Sum('n'))
        years = list(set(queryset.values_list('year', flat=True)))
        years.sort()

        labels = []
        dataspecie_alive = []
        dataspecie_dead = []

        for year in years:
            #for summary in specie_queryset:
            labels.append(year)
            alive = queryset.filter(year=year,alive=True)
            dead = queryset.filter(year=year,alive=False)


            dataspecie_alive.append(alive.aggregate(Sum('n'))["n__sum"]) if alive else dataspecie_alive.append(0)
            dataspecie_dead.append(dead.aggregate(Sum('n'))["n__sum"]) if dead else dataspecie_dead.append(0)

        data.append({
            "specie": specie,
            "labels": labels,
            "datasets": [{
                "label": 'Vivi',
                "maxBarThickness": 50,
                "backgroundColor": "green",
                "data": dataspecie_alive
            }, {
                "label": 'Morti',
                "maxBarThickness": 50,
                "backgroundColor": "red",
                "data": dataspecie_dead
            }]
        })
        
        return Response(data)
