from __future__ import unicode_literals
from django.contrib.auth.forms import UserChangeForm
from wwf_prince.utils import *
from sorl.thumbnail.admin import AdminImageMixin
from .models import Association
from imagekit.cachefiles import ImageCacheFile
from imagekit.processors import ResizeToFill
from imagekit import ImageSpec
from imagekit.admin import AdminThumbnail
from django.db import models
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import admin
from authtools.admin import NamedUserAdmin
from .models import Profile, FreeProfile
from django.contrib.auth import get_user_model
User = get_user_model()

from .forms import UserForm

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['profile_name','user__name']
    ordering = ['user__name']


class UserProfileInline(AdminImageMixin, admin.StackedInline):
    search_fields = ['name']
    model = Profile


class NewUserAdmin(NamedUserAdmin):
    search_fields = ['name',"email"]
    ordering = ['name']
    inlines = [UserProfileInline]
    forms = UserChangeForm    
    list_display = ('is_active', 'email', 'name', 'permalink',
                    'is_superuser', 'is_staff',)

    # 'View on site' didn't work since the original User model needs to
    # have get_absolute_url defined. So showing on the list display
    # was a workaround.
    def permalink(self, obj):
        url = reverse("profiles:show",
                      kwargs={"slug": obj.profile.slug})
        # Unicode hex b6 is the Pilcrow sign
        return format_html('<a href="{}">{}</a>'.format(url, '\xb6'))

@admin.register(Association)
class AssociationAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('__str__', 'website', 'facebook', 'email','image',)
    list_editable = ('website', 'facebook', 'email','image',)

@admin.register(FreeProfile)
class FreeProfileAdmin(admin.ModelAdmin):
    search_fields = ['profile_name',"profile_surname","email"]
    ordering = ['profile_name','profile_surname']
    list_display = ('profile_name', 'profile_surname', 'email', 'association','role',)
    filter_fields = ('association','role','preferred_site',)
    autocomplete_fields = ['preferred_site']
    fieldsets = (
        ('Principali', {
            'fields': (
                ('profile_name','profile_surname',),
                ('email','phone_number',),
                ('province',),
            ),
            #'classes': ('collapse','collapsed',),
        }),
        ('Caratteristiche',{
            'fields': (
                ('association','role',),
                ('role_descr',),
                ('preferred_site','liberatoria',),                
            ),
        })
    )


admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)
