from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter
from .models import Site

class SiteFilter(FilterSet):
    name = CharFilter(field_name='name')
    regione = CharFilter(field_name='regione')
    provincia = CharFilter(field_name='provincia')

    class Meta:
        model = Site
        fields = ['name','regione','provincia']