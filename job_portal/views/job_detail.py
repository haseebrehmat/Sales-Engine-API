from threading import Thread
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from job_portal.filters.job_detail import CustomJobFilter
from job_portal.models import JobDetail
from job_portal.paginations.job_detail import CustomPagination
from job_portal.permissions.job_detail import JobDetailPermission
from job_portal.serializers.job_detail import JobDetailOutputSerializer, JobDetailSerializer


class JobDetailsView(ModelViewSet):
    queryset = JobDetail.objects.filter(job_status=0)
    serializer_class = JobDetailSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    model = JobDetail
    parser_classes = (MultiPartParser, JSONParser)
    pagination_class = CustomPagination
    filterset_class = CustomJobFilter
    ordering = ('-job_posted_date')
    search_fields = ['job_title', 'job_description']
    http_method_names = ['get']
    ordering_fields = ['job_title', 'job_type', 'job_posted_date', 'company_name']
    permission_classes = (JobDetailPermission,)

    # @method_decorator(cache_page(60*2))
    @swagger_auto_schema(responses={200: JobDetailOutputSerializer(many=False)})
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
