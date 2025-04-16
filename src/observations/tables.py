import django_tables2 as tables
from .models import SiteSummary


class SiteSummaryTable(tables.Table):
    class Meta:
        model = SiteSummary
        orderable = True
        fields = ('year', 'specie', 'sex', 'alive')
        template_name = 'django_tables2/bootstrap.html'
