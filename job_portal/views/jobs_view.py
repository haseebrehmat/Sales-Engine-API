from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from job_portal.filters.job_detail import CustomJobFilter
from job_portal.models import JobDetail, AppliedJobStatus, BlockJobCompany
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
    # search_fields = ['job_title']
    http_method_names = ['get']
    ordering_fields = ['job_title', 'job_type', 'job_posted_date', 'company_name', 'updated_at']
    permission_classes = (JobDetailPermission, )
    # permission_classes = (AllowAny, )

    def get_queryset(self):
        job_title = self.request.GET.get('search')
        if job_title:
            self.queryset = self.queryset.filter(job_title__icontains=job_title)
        blocked = self.request.GET.get('blocked')
        blocked_job_companies = list(
            BlockJobCompany.objects.filter(company=self.request.user.profile.company).values_list('company_name',
                                                                                                  flat=True))
        if blocked == "true":
            self.queryset = self.queryset.filter(company_name__in=blocked_job_companies)
        elif blocked == "false":
            self.queryset = self.queryset.exclude(company_name__in=blocked_job_companies)
        return self.queryset


class JobDetailView(APIView):
    serializer_class = JobDetailSerializer
    excluded = ['job_description']
    queryset = JobDetail.objects.defer(*excluded)
    permission_classes = (JobDetailPermission, )
    # permission_classes = (AllowAny, )

    def get(self, request, pk):
        self.serializer_class.Meta.exclude = self.excluded
        qs = self.queryset.filter(id=pk).first()
        if qs:
            serializer = self.serializer_class(qs, many=False)
            verticals = request.user.profile.vertical.all()
            data = {"total_verticals": [{"name": x.name, "identity": x.identity, "id": x.id} for x in verticals]}
            data["total_verticals_count"] = len(data["total_verticals"])
            jobs = AppliedJobStatus.objects.filter(job_id=pk, vertical__in=verticals)
            data["applied_verticals"] = [{"name": x.vertical.name, "identity": x.vertical.identity, "id": x.vertical.id}
                                         for
                                         x in jobs]
            data["job_details"] = serializer.data
            if not data["job_details"]["job_description_tags"]:
                data["job_details"]["job_description_tags"] = qs.job_description
            data["total_applied_count"] = len(data["applied_verticals"])
        else:
            data = []
        return Response(data, status=status.HTTP_200_OK)
