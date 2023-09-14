import uuid
from datetime import datetime, timedelta

import pandas as pd
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.models import User
from authentication.models.team_management import Team
from authentication.permissions.applied_job_permissions import AppliedJobPermission
from authentication.serializers.users import UserSerializer
from job_portal.filters.applied_job import TeamBasedAppliedJobFilter
from job_portal.models import AppliedJobStatus, DownloadLogs
from job_portal.paginations.applied_job import AppliedJobPagination
from job_portal.serializers.applied_job import TeamAppliedJobDetailSerializer
from scraper.utils.thread import start_new_thread
from settings.base import FROM_EMAIL
from utils import upload_to_s3


# Applied View
class AppliedJobView(ListAPIView):
    queryset = AppliedJobStatus.objects.all()
    pagination_class = AppliedJobPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    serializer_class = TeamAppliedJobDetailSerializer
    model = AppliedJobStatus
    filterset_class = TeamBasedAppliedJobFilter
    ordering = ('-applied_date')
    search_fields = ['applied_by']
    ordering_fields = ['applied_date', 'job__job_posted_date']
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            self.request.user = User.objects.get(email__icontains='kaleem@maverickslabs.io')
            bd_id_list = []

            if request.user.roles.name.lower() == "owner":
                queryset = Team.objects.filter(
                    reporting_to__profile__company=request.user.profile.company).select_related()
                for x in queryset:
                    members = [i for i in x.members.values_list("id", flat=True)]
                    bd_id_list.extend(members)

            else:
                teams = Team.objects.filter(members=request.user).values_list("reporting_to", flat=True)
                bd_id_list = Team.objects.filter(reporting_to__in=teams).values("members__id")

            bd_users = User.objects.filter(id__in=bd_id_list).select_related()
            bd_query = UserSerializer(bd_users, many=True)
            job_list = AppliedJobStatus.objects.filter(applied_by__id__in=bd_id_list).select_related()

            queryset = self.filter_queryset(job_list)
            queryset = self.filter_queryset_data(queryset, request)
            if request.GET.get("download", "") == "true":
                if queryset:
                    excluded_params = ['download', 'page', 'ordering', 'page_size', 'applied_by']
                    filters = {x: request.GET[x] for x in request.query_params.keys() if x not in excluded_params}
                    if DownloadLogs.objects.filter(user=request.user, query=filters, created_at__date=datetime.now().date()).exists():
                        message = "Job exports already exists, check logs"
                    else:
                        self.export_csv(queryset, self.request, filters)
                        message = 'Export in progress, Check Logs in a while'
                    status_code = status.HTTP_200_OK
                else:
                    message = {'detail': 'No job exists'}
                    status_code = status.HTTP_406_NOT_ACCEPTABLE
                return Response(message, status_code)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = self.get_paginated_response(serializer.data)
                data.data['team_members'] = bd_query.data
                end_time = datetime.now()
                start_time = end_time - timedelta(hours=12)
                data.data['last_12_hours_count'] = queryset.filter(
                    applied_date__range=[start_time, end_time]).count()

                data.data['job_source_analytics'] = self.get_job_source_count(bd_id_list)
                data.data['job_type_analytics'] = self.get_job_type_count(bd_id_list)

                return data

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Team.DoesNotExist:
            return Response({"detail": "BD list is empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get_job_source_count(self, bd_ids):
        if self.request.GET.get("applied_by", "") != "":
            bd_ids = [self.request.GET.get("applied_by")]

        job_source_count = list(AppliedJobStatus.objects.filter(applied_by_id__in=bd_ids).values(
            'job__job_source').annotate(total_job_source=Count('job__job_source')))

        return job_source_count

    def get_job_type_count(self, bd_ids):
        if self.request.GET.get("applied_by", "") != "":
            bd_ids = [self.request.GET.get("applied_by")]

        job_type_count = list(AppliedJobStatus.objects.filter(applied_by_id__in=bd_ids).values(
            'job__job_type').annotate(total_job_type=Count('job__job_type')))

        return job_type_count

    def filter_queryset_data(self, queryset, request):
        if request.GET.get('tech_stacks'):
            queryset = queryset.filter(job__tech_keywords__in=request.GET.get('tech_stacks').split(','))
        if request.GET.get('start_date'):
            queryset = queryset.filter(converted_at__gte=request.GET.get('start_date'))
        if request.GET.get('end_date'):
            queryset = queryset.filter(converted_at__lte=request.GET.get('end_date'))
        if request.GET.get('applied_by'):
            queryset = queryset.filter(applied_by__id=request.GET.get('applied_by'))
        if request.GET.get('job_source'):
            queryset = queryset.filter(job__job_source__in=request.GET.get('job_source').split(','))

        return queryset

    @start_new_thread
    def export_csv(self, queryset, request, query):
        try:
            data = [
                {
                    "job_title": x.job.job_title,
                    "company_name": x.job.company_name,
                    "job_source": x.job.job_source,
                    "job_type": x.job.job_type,
                    "address": x.job.address,
                    "job_description": x.job.job_description,
                    "tech_keywords": x.job.tech_keywords,
                    "job_posted_date": str(x.job.job_posted_date),
                    "job_source_url": x.job.job_source_url,
                    "applied_by_name": x.applied_by.username,
                    "applied_date": str(x.applied_date),
                    "resume": x.resume,
                } for x in queryset]
            df = pd.DataFrame(data)
            filename = f"{request.user.profile.company.name}-{request.user.email}-{str(datetime.now())}.xlsx".lower()
            df.to_excel(f'job_portal/{filename}', index=True)
            path = f"job_portal/{filename}"

            url = upload_to_s3.upload_job_files(path, filename)
            DownloadLogs.objects.create(url=url, user=request.user, query=query)
            # context = {
            #     "browser": request.META.get("HTTP_USER_AGENT", "Not Available"),  # getting browser name
            #     "username": request.user.username,
            #     "company": "Octagon",
            #     "operating_system": request.META.get("GDMSESSION", "Not Available"),  # getting os name
            #     "download_link": url
            # }
            #
            # html_string = render_to_string("csv_email_template.html", context)
            # msg = EmailMultiAlternatives("Applied Jobs Export", "Applied Jobs Export",
            #                              FROM_EMAIL,
            #                              [request.user.email])
            #
            # msg.attach_alternative(
            #     html_string,
            #     "text/html"
            # )
            # email_status = msg.send()
            # return email_status
            return True
        except Exception as e:
            print("Error in exporting csv function", e)
            return False
