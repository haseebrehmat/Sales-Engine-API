import datetime
import json

from django.contrib.postgres.fields import ArrayField
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Func, CharField, F, Value, TextField
from django.utils import timezone
from rest_framework import pagination
from rest_framework.response import Response

from job_portal.models import JobDetail, BlacklistJobs, BlockJobCompany
from job_portal.utils.job_status import JOB_STATUS_CHOICE


class CustomPagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    query = JobDetail.objects.filter(appliedjobstatus__applied_by=None)
    filtered_query = None
    recruiter_jobs_count = 0
    filtered_jobs_count = 0
    filtered_queryset = None

    def get_paginated_response(self, data, queryset):
        self.filtered_query = queryset
        self.filtered_queryset = self.filter_query(self.query)
        self.filtered_jobs_count = self.page.paginator.count
        self.recruiter_jobs_count = self.get_recruiter_jobs_count()

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
            'filtered_jobs': self.filtered_jobs_count,
            'recruiter_jobs': self.recruiter_jobs_count,
            'non_recruiter_jobs': self.get_non_recruiter_jobs_count(),
            'today_uploaded_jobs': self.get_today_uploaded_jobs_count(),
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
        queryset = self.filtered_queryset

        unique_keyword_object = queryset.extra(select={'name': 'tech_keywords'}).values('name').annotate(
            value=Count('tech_keywords')).exclude(tech_keywords__contains=",")
        unique_count_dic = json.dumps(list(unique_keyword_object), cls=DjangoJSONEncoder)
        unique_count_data = json.loads(unique_count_dic)
        keywords = sorted(unique_count_data, key=lambda x: x["value"], reverse=True)

        return keywords

    def total_job_count(self):
        return JobDetail.objects.count()

    def get_recruiter_jobs_count(self):
        if self.request.GET.get("job_visibility") == "non-recruiter" or self.page.paginator.count == 0:
            return 0
        if self.request.user.profile.company:
            company = BlacklistJobs.objects.filter(company_id=self.request.user.profile.company_id).values_list(
                "company_name", flat=True)
        else:
            company = BlacklistJobs.objects.all().values_list("company_name", flat=True)
        company = list(company)
        queryset = self.filtered_query.filter(company_name__in=company)
        return queryset.count()

    def get_non_recruiter_jobs_count(self):
        if self.request.GET.get("job_visibility") == "recruiter" or self.page.paginator.count == 0:
            return 0
        return self.filtered_jobs_count - self.recruiter_jobs_count

    def get_today_uploaded_jobs_count(self):
        uploaded_jobs = JobDetail.objects.filter(created_at__gte=str(datetime.datetime.today()).split(' ')[0]).count()
        return uploaded_jobs

    def unique_job_source(self):
        unique_job_source = self.filtered_queryset.extra(select={'name': 'job_source'}).values('name').annotate(
            value=Count('tech_keywords'))
        unique_job_source_dic = json.dumps(list(unique_job_source), cls=DjangoJSONEncoder)
        unique_job_data = json.loads(unique_job_source_dic)
        return sorted(unique_job_data, key=lambda x: x["value"], reverse=True)

    def unique_job_type(self):
        unique_job_type = self.filtered_queryset.extra(select={'name': 'job_type'}).values('name').annotate(
            value=Count('job_type'))
        unique_job_type_dic = json.dumps(list(unique_job_type), cls=DjangoJSONEncoder)
        unique_job_type = json.loads(unique_job_type_dic)
        return sorted(unique_job_type, key=lambda x: x["value"], reverse=True)

    def filter_query(self, queryset):
        job_title_params = self.request.GET.get('search')
        if job_title_params:
            queryset = queryset.filter(job_title__icontains=job_title_params)
        if self.request.GET.get("from_date", "") != "":
            from_date = datetime.datetime.strptime(self.request.GET.get("from_date"), "%Y-%m-%d").date()
            queryset = queryset.filter(job_posted_date__gte=from_date)
        if self.request.GET.get("to_date", "") != "":
            to_date = datetime.datetime.strptime(self.request.GET.get("to_date"), "%Y-%m-%d").date()
            queryset = queryset.filter(job_posted_date__lt=to_date+datetime.timedelta(days=1))
        if self.request.GET.get("job_source", "") != "":
            queryset = queryset.filter(job_source__iexact=self.request.GET.get("job_source"))
        if self.request.GET.get("job_type", "") != "":
            queryset = queryset.filter(job_type__iexact=self.request.GET.get("job_type"))
        if self.request.GET.get("tech_keywords", "") != "":
            keywords_list = self.request.GET.get("tech_keywords").split(",")
            queryset = queryset.filter(tech_keywords__in=keywords_list)
        if self.request.GET.get("job_visibility") != "all":
            if self.request.user.profile.company:
                company = BlacklistJobs.objects.filter(company_id=self.request.user.profile.company_id).values_list(
                    "company_name", flat=True)
            else:
                company = BlacklistJobs.objects.all().values_list("company_name", flat=True)
            company = list(company)
            if self.request.GET.get("job_visibility") == "recruiter":
                queryset = queryset.filter(company_name__in=company)
            elif self.request.GET.get("job_visibility") == "non-recruiter":
                queryset = queryset.exclude(company_name__in=company)
        blocked = self.request.GET.get("blocked")
        blocked_job_companies = list(
            BlockJobCompany.objects.filter(company=self.request.user.profile.company).values_list('company_name',
                                                                                                  flat=True))
        if blocked == "true":
            queryset = queryset.filter(company_name__in=blocked_job_companies)
        elif blocked == "false":
            queryset = queryset.exclude(company_name__in=blocked_job_companies)
        return queryset
