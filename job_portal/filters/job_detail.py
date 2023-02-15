import django_filters
from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from job_portal.models import JobDetail


class CustomJobFilter(FilterSet):
    from_date = django_filters.DateFilter(field_name='job_posted_date', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='job_posted_date', lookup_expr='lte')
    job_type = CharFilter(field_name='job_type',lookup_expr='iexact')
    job_source = CharFilter(field_name='job_source',lookup_expr='iexact')
    tech_keywords = CharFilter(field_name='tech_keywords',lookup_expr='iexact')


    class Meta:
        model = JobDetail
        fields = ()