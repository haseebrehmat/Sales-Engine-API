import datetime
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, F
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from job_portal.models import JobDetail, BlockJobCompany, BlacklistJobs
from job_portal.permissions.job_detail import JobDetailPermission


class JobsFilters(APIView):
    permission_classes = (AllowAny,)
    job_sources = set(JobDetail.objects.values_list('job_source', flat=True))
    keywords = set(JobDetail.objects.exclude(tech_keywords__contains=",").values_list('tech_keywords', flat=True))
    queryset = JobDetail.objects.only('job_source', 'job_posted_date').filter(appliedjobstatus__applied_by=None)
    job_types = set(JobDetail.objects.values_list('job_type', flat=True))
    recruiter_jobs_count = 0
    filtered_jobs_count = 0
    filtered_queryset = None

    def get(self, request):
        request.user = User.objects.get(email='admin@gmail.com')
        self.queryset = self.filter_query(self.queryset)
        self.filtered_queryset = self.filter_query(self.queryset)
        self.filtered_jobs_count = self.queryset.count()
        self.recruiter_jobs_count = self.get_recruiter_jobs_count()
        data = {
            'total_jobs': self.total_job_count(),
            'from_date': self.from_date(),
            'to_date': self.to_date(),
            'today_uploaded_jobs': self.get_today_uploaded_jobs_count(),
            'tech_keywords_count_list': self.keyword_count(),
            'job_source_count_list': self.get_job_source_count(),
            'recruiter_jobs': self.recruiter_jobs_count,
            'non_recruiter_jobs': self.get_non_recruiter_jobs_count(),
            'total_job_type': self.get_job_type(),
            'filtered_jobs': self.filtered_jobs_count,
        }

        return Response(data)

    def from_date(self):
        if self.queryset.exists():
            from_date = self.queryset.earliest('job_posted_date').job_posted_date
            return from_date
        else:
            return timezone.datetime.now()

    def to_date(self):
        if self.queryset.exists():
            to_date = self.queryset.latest('job_posted_date').job_posted_date
            return to_date
        else:
            return timezone.datetime.now()

    def get_job_source_count(self):
        filtered_job_sources = self.queryset.values_list("job_source", flat=True)
        self.queryset.values_list("job_source", flat=True)
        job_source_count_list = self.queryset.values('job_source').annotate(
            name=F('job_source'),
            value=Count('job_source')
        ).order_by('-value').values('name', 'value')
        job_source_count_list = list(job_source_count_list)
        for x in self.job_sources:
            if x not in filtered_job_sources:
                job_source_count_list.append({'name': x, 'value': 0})
        return job_source_count_list

    def keyword_count(self):
        filtered_job_sources = self.queryset.values_list("tech_keywords", flat=True)
        unique_keyword_object = list(self.queryset.values('tech_keywords').annotate(
            name=F('tech_keywords'),
            value=Count('tech_keywords')).exclude(tech_keywords__contains=",")
                                     .order_by('-value').values('name', 'value'))
        for x in self.keywords:
            if x not in filtered_job_sources:
                unique_keyword_object.append({'name': x, 'value': 0})

        return unique_keyword_object

    def total_job_count(self):
        return JobDetail.objects.count()

    def get_recruiter_jobs_count(self):
        if self.request.GET.get("job_visibility") == "non-recruiter":
            return 0
        if self.request.user.profile.company:
            company = BlacklistJobs.objects.filter(company_id=self.request.user.profile.company_id).values_list(
                "company_name", flat=True)
        else:
            company = BlacklistJobs.objects.all().values_list("company_name", flat=True)
        company = list(company)
        queryset = self.queryset.filter(company_name__in=company)
        return queryset.count()

    def get_non_recruiter_jobs_count(self):
        if self.request.GET.get("job_visibility") == "recruiter":
            return 0
        return self.queryset.count() - self.recruiter_jobs_count

    def get_today_uploaded_jobs_count(self):
        uploaded_jobs = JobDetail.objects.filter(created_at__gte=str(datetime.datetime.today()).split(' ')[0]).count()
        return uploaded_jobs

    def get_job_type(self):

        unique_job_type = list(self.queryset.values('job_type').annotate(
            name=F('job_type'),
            value=Count('job_type')).values('name', 'value'))

        for x in self.job_types:
            if x not in unique_job_type:
                unique_job_type.append({'name': x, 'value': 0})

        return unique_job_type

    def filter_query(self, queryset):
        job_title_params = self.request.GET.get('search')
        if job_title_params:
            queryset = queryset.filter(job_title__icontains=job_title_params)
        if self.request.GET.get("from_date", "") != "":
            from_date = datetime.datetime.strptime(self.request.GET.get("from_date"), "%Y-%m-%d").date()
            queryset = queryset.filter(job_posted_date__gte=from_date)
        if self.request.GET.get("to_date", "") != "":
            to_date = datetime.datetime.strptime(self.request.GET.get("to_date"), "%Y-%m-%d").date()
            queryset = queryset.filter(job_posted_date__lt=to_date + datetime.timedelta(days=1))
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
