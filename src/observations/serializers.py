from rest_framework import relations
from django.db.models import F,Q
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework_gis.serializers import (
    GeoFeatureModelSerializer
)
from rest_framework_gis.fields import GeometryField
from .models import Specie, Observation, SiteSummary, Site

class DynamicFieldsMixin(object):
    """
    A serializer mixin that takes an additional `fields` argument that controls
    which fields should be displayed.
    Usage::
        class MySerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
            class Meta:
                model = MyModel
    """

    def __init__(self, *args, **kwargs):
        super(DynamicFieldsMixin, self).__init__(*args, **kwargs)
        if not self.context:
            return
        fields = self.context['request'].query_params.get('fields', None)
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class SiteSerializer(DynamicFieldsMixin, GeoFeatureModelSerializer):
    geom = GeometryField()
    class Meta:
        model = Site
        geo_field = 'geom'
        id_field = 'id'
        fields = ['id','name','regione','provincia','comune','descrizione','attivo','geom','lunghezza']



class SpecieSerializer(ModelSerializer):
    class Meta:
        model = Specie
        fields = ('specie', 'vernacular_it')


class SiteSummarySerializer(ModelSerializer):
    class Meta:
        model = SiteSummary
        fields = '__all__'


class ObservationSerializer(ModelSerializer):
    specie_name = serializers.CharField(
        source='specie.specie', read_only=True)
    site_name = serializers.CharField(
        source='session.site.name', read_only=True)
    site_province = serializers.CharField(
        source='session.site.provincia', read_only=True)
    site_region = serializers.CharField(
        source='session.site.regione', read_only=True)
    site_centroid_x = serializers.DecimalField(
        source='session.site.longitude', read_only=True, max_digits=7, decimal_places=5)
    site_centroid_y = serializers.DecimalField(
        source='session.site.latitude', read_only=True, max_digits=7, decimal_places=5)
    session_date = serializers.DateField(
        source='session.date', read_only=True)
    session_begin = serializers.CharField(
        source='session.begin', read_only=True)
    session_end = serializers.CharField(
        source='session.end', read_only=True)
    session_date = serializers.CharField(
        source='session.date', read_only=True)
    session_meteo = serializers.CharField(
        source='session.meteo', read_only=True)
    session_temperature = serializers.FloatField(
        source='session.temperature', read_only=True)
    session_volunteers_registered_n = serializers.IntegerField(
        source='session.volontari_count', read_only=True)
    session_volunteers_unregistered_n = serializers.IntegerField(
        source='session.volontari_unregistered_count', read_only=True)

    class Meta:
        model = Observation
        exclude = ('created_by', 'modified_by', 'created',
                   'modified', 'specie', 'session',)
