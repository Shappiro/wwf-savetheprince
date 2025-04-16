
from django.contrib.gis import admin
from .models import FAQModel, Comuni, Regioni, Province
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe 
from ordered_model.admin import OrderedModelAdmin
from leaflet.admin import LeafletGeoAdminMixin
@admin.register(FAQModel)
class FAQAdmin(OrderedModelAdmin):
    list_display = ('_get_name', 'move_up_down_links')
    list_filter = ['faqtype']

    def _get_name(self, obj):
         return mark_safe(strip_tags(obj.question))
    _get_name.allow_tags = True
    _get_name.short_description = "Domanda"

@admin.register(Comuni)
class ComuniAdmin(admin.ModelAdmin,LeafletGeoAdminMixin):
     search_fields = ['comune']

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin,LeafletGeoAdminMixin):
     search_fields = ['provincia']
     
@admin.register(Regioni)
class RegioniAdmin(admin.ModelAdmin,LeafletGeoAdminMixin):
     search_fields = ['regione']
     
     