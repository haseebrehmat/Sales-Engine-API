import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.utils import timezone
from rest_framework import pagination
from rest_framework.response import Response

from job_portal.models import JobDetail, BlacklistJobs
from job_portal.utils.job_status import JOB_STATUS_CHOICE


class CustomPagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    query = JobDetail.objects.all()

    def get_paginated_response(self, data):
        response = Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'num_pages': self.page.paginator.num_pages
            },
            'from_date': self.from_date(),
            'to_date': self.to_date(),
            'total_jobs': self.total_job_count(),
            'total_job_type': self.unique_job_type(),
            'filtered_jobs': self.page.paginator.count,
            'data': data,
            'tech_keywords_count_list': self.keyword_count(),
            'job_source_count_list': self.unique_job_source(),
            'job_status_choice': dict(JOB_STATUS_CHOICE)
        })
        return response

    def from_date(self):
        if self.query:
            from_date = self.query.earliest('job_posted_date').job_posted_date
            return from_date
        else:
            return timezone.datetime.now()

    def to_date(self):
        if self.query:
            to_date = self.query.latest('job_posted_date').job_posted_date
            return to_date
        else:
            return timezone.datetime.now()

    def keyword_count(self):
        queryset = JobDetail.objects.filter(appliedjobstatus__applied_by=None)
        queryset = self.filter_query(queryset)

        unique_keyword_object = queryset.extra(select={'name': 'tech_keywords'}).values('name').annotate(
            value=Count('tech_keywords'))

        unique_count_dic = json.dumps(list(unique_keyword_object), cls=DjangoJSONEncoder)
        unique_count_data = json.loads(unique_count_dic)
        keywords = sorted(unique_count_data, key=lambda x: x["value"], reverse=True)

        return keywords

    def total_job_count(self):
        job_count = JobDetail.objects.filter(appliedjobstatus__applied_by=None).count()
        return job_count

    def unique_job_source(self):
        queryset = JobDetail.objects.filter(appliedjobstatus__applied_by=None)
        queryset = self.filter_query(queryset)
        unique_job_source = queryset.extra(select={'name': 'job_source'}).values('name').annotate(
            value=Count('tech_keywords'))
        unique_job_source_dic = json.dumps(list(unique_job_source), cls=DjangoJSONEncoder)
        unique_job_data = json.loads(unique_job_source_dic)
        return sorted(unique_job_data, key=lambda x: x["value"], reverse=True)

    def unique_job_type(self):
        queryset = JobDetail.objects.filter(appliedjobstatus__applied_by=None)
        queryset = self.filter_query(queryset)
        unique_job_type = queryset.extra(select={'name': 'job_type'}).values('name').annotate(
            value=Count('job_type'))
        unique_job_type_dic = json.dumps(list(unique_job_type), cls=DjangoJSONEncoder)
        unique_job_type = json.loads(unique_job_type_dic)
        return sorted(unique_job_type, key=lambda x: x["value"], reverse=True)

    def filter_query(self, queryset):
        if self.request.GET.get("from_date", "") != "":
            queryset = queryset.filter(job_posted_date__gte=self.request.GET.get("from_date"))
        if self.request.GET.get("to_date", "") != "":
            queryset = queryset.filter(job_posted_date__lte=self.request.GET.get("to_date"))
        # if self.request.GET.get("job_source", "") != "":
        #     queryset = queryset.filter(job_source__iexact=self.request.GET.get("job_source"))
        if self.request.GET.get("job_type", "") != "":
            queryset = queryset.filter(job_type__iexact=self.request.GET.get("job_type"))
        # if self.request.GET.get("job_visibility", "all") != "all":
        #     company = BlacklistJobs.objects.filter(company_id=self.request.user.profile.company_id).values_list(
        #         "company_name", flat=True)
        #     company = list(company)
        #     if self.request.GET.get("job_visibility", "all") == "non-recruiter":
        #         queryset = queryset.exclude(company_name__in=company)
        #     elif self.request.GET.get("job_visibility", "all") == "recruiter":
        #         queryset = queryset.filter(company_name__in=company)
        return queryset
