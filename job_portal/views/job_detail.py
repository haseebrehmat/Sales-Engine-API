import uuid

import pandas as pd
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count, Q
from django.db import transaction
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import JSONParser, MultiPartParser

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from authentication.models.user import User

from job_portal.filters.job_detail import CustomJobFilter
from job_portal.models import JobDetail, AppliedJobStatus, BlacklistJobs, BlockJobCompany, JobArchive
from job_portal.utils.detect_changes import detect_model_changes
from job_portal.paginations.job_detail import CustomPagination
from job_portal.permissions.job_detail import JobDetailPermission
from job_portal.serializers.job_detail import JobDetailOutputSerializer, JobDetailSerializer
from scraper.utils.thread import start_new_thread
from settings.base import FROM_EMAIL
from settings.utils.custom_pagination import CustomCursorPagination
from utils import upload_to_s3

from authentication.exceptions import InvalidUserException
from settings.utils.helpers import serializer_errors
import re

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')


class JobDetailsView(ModelViewSet):
    queryset = JobDetail.objects.only('id')
    serializer_class = JobDetailSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    model = JobDetail
    parser_classes = (MultiPartParser, JSONParser)
    pagination_class = CustomPagination
    filterset_class = CustomJobFilter
    ordering = ('-job_posted_date',)
    search_fields = ['job_title', 'company_name']
    http_method_names = ['get']
    ordering_fields = ['job_title', 'job_type', 'job_posted_date', 'company_name']
    permission_classes = (JobDetailPermission,)

    def get_paginated_response(self, data, query):
        return self.paginator.get_paginated_response(data, query)

    # @swagger_auto_schema(responses={200: JobDetailOutputSerializer(many=False)})
    def list(self, request, *args, **kwargs):
        if self.queryset.count() == 0:
            return Response([], status=200)

        current_user = request.user

        current_user_jobs_list = AppliedJobStatus.objects.filter(applied_by=current_user).only('job_id', 'applied_by')

        if current_user_jobs_list:
            excluded_jobs = self.get_applied_jobs(current_user, current_user_jobs_list)
            queryset = self.get_queryset().exclude(id__in=excluded_jobs)
        else:
            queryset = self.get_queryset()
        # filter blocked job company
        queryset = self.filter_blocked_job_company(queryset)

        # pass the queryset to the remaining filters
        queryset = self.filter_queryset(queryset)

        # handle job search with exact match of job title
        job_title_params = self.request.GET.get('search')

        if job_title_params:
            queryset = queryset.filter(
                Q(job_title__icontains=job_title_params) | Q(company_name__icontains=job_title_params)
            )

        # Exporting CSV Data
        if request.GET.get("download", "") == "true":
            self.export_csv(queryset, self.request)
            return Response("Export in progress, You will be notify through email")

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            self.update_serializer_for_blacklist_jobs(serializer)
            return self.get_paginated_response(serializer.data, queryset)

        serializer = self.get_serializer(queryset, many=True)

        serializer = self.update_serializer_for_blacklist_jobs(serializer)

        return Response(serializer.data)

    def get_blacklist_companies(self):
        if self.request.user.profile.company:
            company = self.request.user.profile.company
            blacklist_companies = list(BlacklistJobs.objects.filter(company_id=company.id).values_list(
                "company_name", flat=True))
        else:
            blacklist_companies = list(BlacklistJobs.objects.all().values_list("company_name", flat=True))
        blacklist_companies = [c.lower() for c in blacklist_companies if c]
        return blacklist_companies

    def update_serializer_for_blacklist_jobs(self, serializer):
        blocked_companies = self.get_blacklist_companies()
        for data in serializer.data:
            if data['company_name'] in blocked_companies:
                data['block'] = True
            else:
                data['block'] = False
        return serializer

    def get_applied_jobs(self, user, job_list):
        verticals = user.profile.vertical.all()

        excluded_list = job_list.values_list('job_id', flat=True)
        excluded_list = [str(x) for x in excluded_list
                         if AppliedJobStatus.objects.filter(job_id=str(x),
                                                            vertical__in=verticals).count() >= verticals.count()]
        return excluded_list

    @start_new_thread
    def export_csv(self, queryset, request):
        try:
            values_list = [
                "job_title",
                "company_name",
                "job_source",
                "job_type",
                "address",
                "job_description",
                "tech_keywords",
                "job_posted_date",
                "job_source_url",
            ]
            data = list(queryset.values(*values_list))
            df = pd.DataFrame(data)
            filename = "export-" + str(uuid.uuid4())[:10] + ".xlsx"
            df.to_excel(f'job_portal/{filename}', index=True)
            path = f"job_portal/{filename}"

            url = upload_to_s3.upload_csv(path, filename)
            context = {
                "browser": request.META.get("HTTP_USER_AGENT", "Not Available"),  # getting browser name
                "username": request.user.username,
                "company": "Octagon",
                "operating_system": request.META.get("GDMSESSION", "Not Available"),  # getting os name
                "download_link": url
            }

            html_string = render_to_string("csv_email_template.html", context)
            msg = EmailMultiAlternatives("Jobs Export", "Jobs Export",
                                         FROM_EMAIL,
                                         [request.user.email])

            msg.attach_alternative(
                html_string,
                "text/html"
            )
            email_status = msg.send()
            return email_status
        except Exception as e:
            print("Error in exporting csv function", e)
            return False

    def filter_blocked_job_company(self, queryset):
        blocked_job_companies = list(
            BlockJobCompany.objects.filter(company=self.request.user.profile.company).values_list('company_name',
                                                                                                  flat=True))
        blocked = self.request.GET.get('blocked')
        if blocked == "true":
            queryset = queryset.filter(company_name__in=blocked_job_companies)
        elif blocked == "false":
            queryset = queryset.exclude(company_name__in=blocked_job_companies)
        return queryset


class RemoveDuplicateView(APIView):

    def post(self, request):
        if request.user.is_superuser:
            self.remove_duplicate()
            message = "Duplication removal in progress"
        else:
            message = "Only Admin has access to this endpoint"
        return Response({"detail": message}, status=201)

    @start_new_thread
    @transaction.atomic
    def remove_duplicate(self):
        print("Getting Duplicates!")
        try:
            duplicate_values = JobDetail.objects.values('company_name', 'job_title', 'job_applied').annotate(
                count=Count('id')).filter(count__gt=1)

            for duplicate in duplicate_values:
                # Get all the duplicate records
                duplicate_records = JobDetail.objects.filter(company_name=duplicate['company_name'],
                                                            job_title=duplicate['job_title'],
                                                            job_applied=duplicate['job_applied']
                                                            )

                # Keep the first record and delete the rest
                first_record = duplicate_records.first()
                duplicate_records.exclude(pk=first_record.pk).delete()
            print("Duplicates Removed!")
        except:
            print("")


class JobModification(APIView):
    def put(self, request, pk):
        conditions = [
            request.data.get("job_title", "") != "",
            request.data.get("company_name", "") != "",
            request.data.get("job_source", "") != "",
            request.data.get("job_type", "") != "",
            request.data.get("address", "") != "",
            request.data.get("job_posted_date", "") != "",
            request.data.get("job_source_url", "") != "",
            request.data.get("tech_keywords", "") != "",
            request.data.get("expired", "") != "",
            request.data.get("time", "") != "",
            request.data.get("job_description_tags", "") != ""
        ]

        if all(conditions):
            query = JobDetail.objects.filter(pk=pk)
            if query.exists():
                queryset = query.first()
                raw_data = request.data.get('job_description_tags')
                request.data['job_description'] = re.sub(CLEANR, '', raw_data)

                if request.data['expired'] == True:
                    request.data['expired_at'] = datetime.now()
                else:
                    request.data['expired_at'] = None

                request.data['job_role'] = request.data.get("job_role") if request.data.get(
                    "job_role") else queryset.job_role
                request.data['salary_max'] = request.data.get("salary_max") if request.data.get(
                    "salary_max") else queryset.salary_max
                request.data['salary_min'] = request.data.get("salary_min") if request.data.get(
                    "salary_min") else queryset.salary_min
                request.data['salary_format'] = request.data.get("salary_format") if request.data.get(
                    "salary_format") else queryset.salary_format
                serializer = JobDetailSerializer(queryset, data=request.data)
                if serializer.is_valid():
                    # Here is a logic of detect changes module
                    time = request.data.pop("time")
                    expired = request.data.pop("expired")
                    job_posted_date = request.data.pop("job_posted_date")
                    detect_model_changes(queryset, request.data, JobDetail, request.user)
                    request.data['time'] = time
                    request.data["expired"] = expired
                    posted_at = f'{job_posted_date} {time}'
                    serializer.validated_data["job_posted_date"] = datetime.strptime(posted_at,
                                                                        "%Y-%m-%d %H:%M")

                    serializer.validated_data['edited'] = True
                    serializer.save()
                    status_code = status.HTTP_200_OK
                    message = {"detail": "Job updated successfully"}
                    return Response(message, status=status_code)
                data = serializer_errors(serializer)
                raise InvalidUserException(data)
            return Response({"detail": "This job does not exist"},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Feilds cannot be empty"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk):
        job_archive = JobDetail.objects.filter(pk=pk)
        if job_archive.exists():
            archive = job_archive.first()
            JobArchive.objects.create(job_title=archive.job_title, company_name=archive.company_name,
                                      job_source=archive.job_source, job_type=archive.job_type, address=archive.address,
                                      job_description=archive.job_description, tech_keywords=archive.tech_keywords,
                                      job_posted_date=archive.job_posted_date, job_source_url=archive.job_source_url,
                                      block=archive.block, is_manual=archive.is_manual)
            archive.delete()
            message = {"detail": "Job deleted successfully"}
            return Response(message, status=status.HTTP_200_OK)
        return Response({"detail": "This job does not exist"},
                        status=status.HTTP_404_NOT_FOUND)


class MarkedAsExpiredView(ModelViewSet):
    queryset = JobDetail.objects.exclude(expired_at=None)
    serializer_class = JobDetailSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    model = JobDetail
    parser_classes = (MultiPartParser, JSONParser)
    pagination_class = CustomPagination
    filterset_class = CustomJobFilter
    ordering = ('-job_posted_date',)
    search_fields = ['job_title']
    http_method_names = ['get']
    ordering_fields = ['job_title', 'job_type', 'job_posted_date', 'company_name']
    permission_classes = (JobDetailPermission,)

    def get_paginated_response(self, data, query):
        return self.paginator.get_paginated_response(data, query)

    @swagger_auto_schema(responses={200: JobDetailOutputSerializer(many=False)})
    def list(self, request, *args, **kwargs):
        if self.queryset.count() == 0:
            return Response([], status=200)

        current_user = request.user

        current_user_jobs_list = AppliedJobStatus.objects.filter(applied_by=current_user).select_related('applied_by')

        if current_user_jobs_list:
            excluded_jobs = self.get_applied_jobs(current_user, current_user_jobs_list)
            queryset = self.get_queryset().exclude(id__in=excluded_jobs)
        else:
            queryset = self.get_queryset()
        # filter blocked job company
        queryset = self.filter_blocked_job_company(queryset)

        # pass the queryset to the remaining filters
        queryset = self.filter_queryset(queryset)

        # handle job search with exact match of job title
        job_title_params = self.request.GET.get('search')

        if job_title_params:
            queryset = queryset.filter(job_title__icontains=job_title_params)

        # Exporting CSV Data
        if request.GET.get("download", "") == "true":
            self.export_csv(queryset, self.request)
            return Response("Export in progress, You will be notify through email")

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            self.update_serializer_for_blacklist_jobs(serializer)
            return self.get_paginated_response(serializer.data, queryset)

        serializer = self.get_serializer(queryset, many=True)

        serializer = self.update_serializer_for_blacklist_jobs(serializer)

        return Response(serializer.data)

    def get_blacklist_companies(self):
        if self.request.user.profile.company:
            company = self.request.user.profile.company
            blacklist_companies = list(BlacklistJobs.objects.filter(company_id=company.id).values_list(
                "company_name", flat=True))
        else:
            blacklist_companies = list(BlacklistJobs.objects.all().values_list("company_name", flat=True))
        blacklist_companies = [c.lower() for c in blacklist_companies if c]
        return blacklist_companies

    def update_serializer_for_blacklist_jobs(self, serializer):
        blocked_companies = self.get_blacklist_companies()
        for data in serializer.data:
            if data['company_name'] in blocked_companies:
                data['block'] = True
            else:
                data['block'] = False
        return serializer

    def get_applied_jobs(self, user, job_list):
        verticals = user.profile.vertical.all()

        excluded_list = job_list.values_list('job_id', flat=True)
        excluded_list = [str(x) for x in excluded_list
                         if AppliedJobStatus.objects.filter(job_id=str(x),
                                                            vertical__in=verticals).count() >= verticals.count()]
        return excluded_list

    @start_new_thread
    def export_csv(self, queryset, request):
        try:
            values_list = [
                "job_title",
                "company_name",
                "job_source",
                "job_type",
                "address",
                "job_description",
                "tech_keywords",
                "job_posted_date",
                "job_source_url",
            ]
            data = list(queryset.values(*values_list))
            df = pd.DataFrame(data)
            filename = "export-" + str(uuid.uuid4())[:10] + ".xlsx"
            df.to_excel(f'job_portal/{filename}', index=True)
            path = f"job_portal/{filename}"

            url = upload_to_s3.upload_csv(path, filename)
            context = {
                "browser": request.META.get("HTTP_USER_AGENT", "Not Available"),  # getting browser name
                "username": request.user.username,
                "company": "Octagon",
                "operating_system": request.META.get("GDMSESSION", "Not Available"),  # getting os name
                "download_link": url
            }

            html_string = render_to_string("csv_email_template.html", context)
            msg = EmailMultiAlternatives("Jobs Export", "Jobs Export",
                                         FROM_EMAIL,
                                         [request.user.email])

            msg.attach_alternative(
                html_string,
                "text/html"
            )
            email_status = msg.send()
            return email_status
        except Exception as e:
            print("Error in exporting csv function", e)
            return False

    def filter_blocked_job_company(self, queryset):
        blocked_job_companies = list(
            BlockJobCompany.objects.filter(company=self.request.user.profile.company).values_list('company_name',
                                                                                                  flat=True))
        blocked = self.request.GET.get('blocked')
        if blocked == "true":
            queryset = queryset.filter(company_name__in=blocked_job_companies)
        elif blocked == "false":
            queryset = queryset.exclude(company_name__in=blocked_job_companies)
        return queryset
