from threading import Thread
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from job_portal.filters.job_detail import CustomJobFilter
from job_portal.models import JobDetail, AppliedJobStatus, BlacklistJobs
from job_portal.paginations.job_detail import CustomPagination
from job_portal.permissions.job_detail import JobDetailPermission
from job_portal.serializers.job_detail import JobDetailOutputSerializer, JobDetailSerializer


class JobDetailsView(ModelViewSet):
    queryset = JobDetail.objects.all()
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

    # @method_decorator(cache_page(60*2))
    @swagger_auto_schema(responses={200: JobDetailOutputSerializer(many=False)})
    def list(self, request, *args, **kwargs):
        if self.queryset.count() == 0:
            return Response([], status=200)

        current_user = request.user

        current_user_jobs_list = AppliedJobStatus.objects.select_related('applied_by').filter(applied_by=current_user)

        if len(current_user_jobs_list) > 0:
            excluded_jobs = self.get_applied_jobs(current_user, current_user_jobs_list)
            queryset = self.get_queryset().exclude(id__in=excluded_jobs)
        else:
            queryset = self.get_queryset()
        # pass the queryset to the remaining filters
        queryset = self.filter_queryset(queryset)

        # handle job search with exact match of job title
        job_title_params = self.request.GET.get('search')

        if job_title_params:
            queryset = queryset.filter(job_title__icontains=job_title_params)

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
