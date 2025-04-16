from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
import profiles.urls
import accounts.urls
import observations.urls
import news.urls
from . import views
from filebrowser.sites import site
from ajax_select import urls as ajax_select_urls

from accounts.views import LoginView as profileLoginView, ProvincesAutoComplete

from observations import views as observations_views

from rest_framework import routers


class HomeAPISaveThePrinceView(routers.APIRootView):
    """
    Da qua si può accedere alle varie risorse per i programmatori che il sito mette a disposizione
    """
    pass


class DocumentedRouter(routers.DefaultRouter):
    APIRootView = HomeAPISaveThePrinceView


router = DocumentedRouter()
router.register(r'sites', observations_views.SiteViewSet)
router.register(r'observations', observations_views.ObservationViewSet)
router.register(r'sitesummaries', observations_views.SiteSummaryViewSet)


# Personalized admin site settings like title and header
admin.site.site_title = 'Amministrazione sito Save the Prince'
admin.site.site_header = 'Amministrazione sito'

handler404 = "wwf_prince.views.page_not_found_view"
handler403 = "wwf_prince.views.unauthorized_view"
#handler500 = "wwf_prince.views.server_error_view"

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('admin/filebrowser/', site.urls),
    path('ajax_select/', include(ajax_select_urls)),
    path('chi_siamo/', views.AboutPage.as_view(), name='about'),
    path('faq/', views.FAQPage.as_view(), name='faq'),
    path('amici/', views.FriendsPage.as_view(), name='friends'),
    path('giornali/', views.JournalsPage.as_view(), name='journals'),
    path('utenti/', include(profiles.urls)),
    # path('', include('dbbackup_ui.urls')),
    path('admin/login/', profileLoginView.as_view(),name='adminlogin'),
    path('admin/', admin.site.urls),
    path('progetto/', views.ProjectPage.as_view(), name='project'),
    path('siti/', views.SitesPage.as_view(), name='sites'),
    path('manuale/', views.ManualPage.as_view(), name='manual'),
    path('dati/', views.DataPage.as_view(), name='data'),
    path('contatti/', views.ContactsPage.as_view(), name='contacts'),
    path('biblio/', views.BibliographyPage.as_view(), name='biblio'),
    path('grafici/', observations_views.GraphPage.as_view(), name='graph'),
    path('contribuisci/', views.ContributePage.as_view(), name='contribute'),
    path('tinymce/', include('tinymce.urls')),
    path('', include(accounts.urls)),
    path('osservazioni/', include(observations.urls)),
    path('posts/', include(news.urls)),
    path('provinces-autocomplete/',ProvincesAutoComplete.as_view(),name='provinces-autocomplete'),
    path('api/', include(router.urls)),
    path('api/sites/',
         observations_views.SiteViewSet.as_view({'get': 'list'}), name='sites-list'),
    path('api/chart/data/', observations_views.ChartData.as_view(),
         name='chart'),
    path('api/chart/effortdata/', observations_views.ChartEffortData.as_view(),
         name='chart-effort'),
    path('api/chart/yearlydirectionspecie/', observations_views.ChartYearlyDirectionSpecieData.as_view(),
         name='chart-yearlydirectionspecie'),
    path('api/chart/yearlydeadalivespecie/', observations_views.ChartYearlyDeadAliveSpecieData.as_view(),
         name='chart-yearlydeadalivespecie'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Include django debug toolbar if DEBUG is on
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
