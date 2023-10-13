import django_filters
from django.db.models import Q
from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from job_portal.models import JobDetail, BlacklistJobs
import datetime


class CustomJobFilter(FilterSet):
    from_date = django_filters.DateFilter(method='from_date_field', field_name='job_posted_date')
    to_date = django_filters.DateFilter(method='to_date_field', field_name='job_posted_date')
    job_type = CharFilter(method='job_type_field', field_name='job_type')
    # job_source = CharFilter(field_name='job_source', lookup_expr='iexact')
    job_source = CharFilter(method='job_sources_field', field_name='job_source', lookup_expr='iexact')
    # tech_keywords = CharFilter(field_name='tech_keywords',lookup_expr='iexact')
    tech_keywords = CharFilter(method='tech_keywords_field', field_name='tech_keywords', lookup_expr='iexact')
    job_visibility = CharFilter(method='filter_company', field_name='job_visibility')
    job_title = CharFilter(field_name='job_title', lookup_expr='iexact')

    class Meta:
        model = JobDetail
        fields = ()

    def from_date_field(self, queryset, field_name, value):
        if value:
            queryset = queryset.filter(job_posted_date__gte=value)
        return queryset

    def to_date_field(self, queryset, field_name, value):
        from_date = self.request.GET.get('from_date')
        to_date = self.request.GET.get('to_date')
        if value:
            queryset = queryset.filter(job_posted_date__lt=value + datetime.timedelta(days=1))
        return queryset

    def tech_keywords_field(self, queryset, field_name, value):
        if value and value != "":
            keywords_list = value
            if isinstance(value, str):
                keywords_list = value.split(",")
                keyword_filters = Q()
                for x in keywords_list:
                    keyword_filters |= Q(tech_stacks__contains=[x])
            return queryset.filter(keyword_filters)
        return queryset

    def job_sources_field(self, queryset, field_name, value):
        if value and value != "":
            keyword_list = value.split(",")
            return queryset.filter(job_source__in=keyword_list)
        return queryset

    def job_type_field(self, queryset, field_name, value):
        if value and value != "":
            keyword_list = value.split(",")
            return queryset.filter(job_type__in=keyword_list)
        return queryset

    def filter_company(self, queryset, field_name, value):
        # all
        # recruiter
        # non-recruiter

        value = value.lower()

        company = self.request.user.profile.company
        if company:
            blacklist_company = list(BlacklistJobs.objects.filter(company_id=company.id).values_list(
                "company_name", flat=True))
        else:
            blacklist_company = list(BlacklistJobs.objects.all().values_list("company_name", flat=True))

        blacklist_company = [c.lower() for c in blacklist_company if c]

        if value == 'recruiter':
            return queryset.filter(company_name__in=blacklist_company)

        elif value == 'non-recruiter':
            queryset = queryset.exclude(company_name__in=blacklist_company)

        return queryset
