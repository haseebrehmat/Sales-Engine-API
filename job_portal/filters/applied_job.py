import django_filters
from django_filters.rest_framework import FilterSet

from job_portal.models import AppliedJobStatus


class CustomAppliedJobFilter(FilterSet):
    job_status = django_filters.NumberFilter(field_name='job__job_status', lookup_expr='exact')

    class Meta:
        model = AppliedJobStatus
        fields = ()