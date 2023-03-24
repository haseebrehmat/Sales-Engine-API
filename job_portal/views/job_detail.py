from threading import Thread
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from job_portal.filters.job_detail import CustomJobFilter
from job_portal.models import JobDetail, AppliedJobStatus
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
    ordering = ('-job_posted_date')
    search_fields = ['job_title']
    http_method_names = ['get']
    ordering_fields = ['job_title', 'job_type', 'job_posted_date', 'company_name']
    permission_classes = (JobDetailPermission,)

    # @method_decorator(cache_page(60*2))
    @swagger_auto_schema(responses={200: JobDetailOutputSerializer(many=False)})
    def list(self, request, *args, **kwargs):
        current_user = request.user

        current_user_jobs_list = AppliedJobStatus.objects.select_related('applied_by').filter(applied_by=current_user)
        if len(current_user_jobs_list) > 0:
            queryset = self.get_queryset().exclude(id__in=current_user_jobs_list.values_list('job_id', flat=True))
        else:
            queryset = self.get_queryset()
        # pass the queryset to the remaining filters
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
