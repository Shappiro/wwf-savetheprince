from ajax_select import register, LookupChannel
from profiles.models import Profile, Site
from django.db.models import Q

@register('profiles')
class ProfileLookup(LookupChannel):
    model = Profile
    def get_query(self, q, request):
        return self.model.objects.filter(Q(user__name__icontains=q) | Q(profile_name__icontains=q) | Q(profile_surname__icontains=q)).order_by('user__name')[:5]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.user.name

@register('sites')
class SitesLookup(LookupChannel):
    model = Site
    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('name')[:5]

    def format_item_display(self, item):
        return u"<span class='tag'>{} ({})</span>".format(item.name,item.comune) 