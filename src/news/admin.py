from django.contrib.gis import admin
from imagekit.admin import AdminThumbnail

from wwf_prince.utils import *

from sorl.thumbnail.admin import AdminImageMixin
from leaflet.admin import LeafletGeoAdmin
from leaflet.admin import LeafletGeoAdminMixin

from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','date','get_association_name',)
    #readonly_fields = ('user',)

    search_fields = ('name',)
    list_filter = ('association__name','site__name',)
    ordering = ('date',)

    def get_association_name(self,obj):
        if obj.association:
            return obj.association.name
        else:
            return ''
    get_association_name.short_description = 'Associazione'
    
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)