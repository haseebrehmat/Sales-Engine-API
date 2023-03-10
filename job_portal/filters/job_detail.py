import json

import django_filters
from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from job_portal.models import JobDetail, BlacklistJobs


class CustomJobFilter(FilterSet):
    from_date = django_filters.DateFilter(field_name='job_posted_date', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='job_posted_date', lookup_expr='lte')
    job_type = CharFilter(field_name='job_type',lookup_expr='iexact')
    job_source = CharFilter(field_name='job_source',lookup_expr='iexact')
    # tech_keywords = CharFilter(field_name='tech_keywords',lookup_expr='iexact')
    tech_keywords = CharFilter(method='tech_keywords_field',field_name='tech_keywords')
    job_visibility = CharFilter(method='filter_company',field_name='job_visibility')
    job_title = CharFilter(field_name='job_title',lookup_expr='iexact')


    class Meta:
        model = JobDetail
        fields = ()

    def tech_keywords_field(self, queryset, field_name, value):
        if value and value != "":
            keyword_list = value.split(",")
            return queryset.filter(tech_keywords__iregex=r'(' + '|'.join(keyword_list) + ')')
        return queryset
    def filter_company(self, queryset, field_name, value):
        # all
        # recruiter
        # non-recruiter
        blacklist_company = [i.company_name for i in BlacklistJobs.objects.all()]
        if value == 'recruiter':
            if len(blacklist_company) == 0:
                return JobDetail.objects.none()

            else:
                queryset = queryset.filter(company_name__iregex=r'(' + '|'.join(blacklist_company) + ')')
                return queryset
        
        elif value == 'non-recruiter':
            if len(blacklist_company) == 0:
                return queryset
            else:
                queryset = queryset.exclude(company_name__iregex=r'(' + '|'.join(blacklist_company) + ')')
                return queryset
        else:
            return queryset