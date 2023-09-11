from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from job_portal.filters.job_detail import CustomJobFilter
from job_portal.models import JobDetail
from job_portal.permissions.job_detail import JobDetailPermission
from job_portal.serializers.job_detail import JobDetailSerializer
from settings.utils.custom_pagination import CustomCursorPagination


class JobsView(ListAPIView):
    serializer_class = JobDetailSerializer
    excluded_fields = serializer_class.Meta.exclude
    queryset = JobDetail.objects.defer(*excluded_fields)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    pagination_class = CustomCursorPagination
    filterset_class = CustomJobFilter
    ordering = ('-job_posted_date',)
    search_fields = ['job_title', 'company_name']
    http_method_names = ['get']
    ordering_fields = ['job_title', 'job_type', 'job_posted_date', 'company_name']
    permission_classes = (JobDetailPermission, )

    def get_queryset(self):
        self.request.user = User.objects.get(email='admin@gmail.com')       # for testing
        return self.queryset


class JobDetailView(APIView):
    serializer_class = JobDetailSerializer
    excluded = ['job_description']
    queryset = JobDetail.objects.defer(*excluded)
    permission_classes = (JobDetailPermission, )

    def get(self, request, pk):
        self.serializer_class.Meta.exclude = self.excluded
        qs = self.queryset.filter(id=pk).first()
        if qs:
            serializer = self.serializer_class(qs, many=False)
            data = serializer.data
        else:
            data = []
        return Response(data, status=status.HTTP_200_OK)
