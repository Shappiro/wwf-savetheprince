from django.urls import path
from . import views

urlpatterns = [
    path('', views.DataPage.as_view(), name='data'),
    path('site/', views.site_new, name='site_new'),
    path('site/species', views.site_species, name='site_species'),
    path('site-autocomplete/',views.SiteAutoComplete.as_view(),name='site-autocomplete'),
    path('profile-autocomplete/',views.ProfileAutoComplete.as_view(),name='profile-autocomplete'),
    path('site-autocomplete-grouped/',views.SiteAutoCompleteGrouped.as_view(),name='site-autocomplete-grouped'),
    path('site-summary/',views.SiteAutoCompleteGrouped.as_view(),name='site-summary'),
    path('yearly-report/<pk>', views.YearlyReportDetail.as_view(), name='yearlyreport-detail')    
]