import datetime
import uuid

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from authentication.models import TeamRoleVerticalAssignment
from job_portal.filters.applied_job import CustomAppliedJobFilter
from job_portal.models import AppliedJobStatus
from job_portal.paginations.applied_job import AppliedJobPagination
from job_portal.permissions.applied_job_detail import AppliedJobDetailPermission
from job_portal.serializers.applied_job import AppliedJobDetailSerializer


class AppliedJobDetailsView(ListAPIView):
    queryset = AppliedJobStatus.objects.all()
    pagination_class = AppliedJobPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    serializer_class = AppliedJobDetailSerializer
    model = AppliedJobStatus
    filterset_class = CustomAppliedJobFilter
    ordering = ('-applied_date',)
    search_fields = ['job__job_title', 'job__job_description', 'job__tech_keywords', 'job__job_type']
    ordering_fields = ['job__tech_keywords', 'job__job_type', 'job__job_posted_date', 'applied_date']
    permission_classes = (AppliedJobDetailPermission,)

    # @method_decorator(cache_page(60*2))
    @swagger_auto_schema(responses={200: AppliedJobDetailSerializer(many=False)})
    def get(self, request, *args, **kwargs):
        excluded_verticals_ids = (TeamRoleVerticalAssignment.objects.filter(role=request.user.roles, member=request.user)
                                  .values_list('vertical_id', flat=True))
        user_id = request.query_params.get('user_id', None)
        filter_query = self.get_queryset()
        if self.is_valid_uuid(user_id):
            filter_query = filter_query.filter(applied_by__id=user_id, vertical_id__in=excluded_verticals_ids)
        queryset = self.filter_queryset(filter_query)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data)
            start_time = datetime.datetime.now() - datetime.timedelta(hours=12)
            end_time = datetime.datetime.now()
            count = filter_query.filter(applied_date__range=[start_time, end_time]).count()
            paginated_data.data["last_12_hours_count"] = count

            return paginated_data

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def is_valid_uuid(self, val):
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False
