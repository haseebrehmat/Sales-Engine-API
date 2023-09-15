import django_filters
from django_filters.rest_framework import FilterSet
from job_portal.models import AppliedJobStatus


class CustomJobFilter(FilterSet):
    applied_by = django_filters.UUIDFilter(field_name='applied_by__id', lookup_expr='exact')
    from_date = django_filters.DateFilter(field_name='applied_date', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='applied_date', lookup_expr='lte')

    class Meta:
        model = AppliedJobStatus
        fields = ()
