from datetime import datetime, timedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from authentication.models import User
from authentication.models.team_management import Team
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from authentication.serializers.users import UserSerializer
from job_portal.filters.applied_job import TeamBasedAppliedJobFilter
from job_portal.models import AppliedJobStatus
from job_portal.paginations.applied_job import AppliedJobPagination
from job_portal.permissions.team_applied_job import TeamAppliedJobPermission
from job_portal.serializers.applied_job import TeamAppliedJobDetailSerializer


class ListAppliedJobView(ListAPIView):
    queryset = AppliedJobStatus.objects.all()
    pagination_class = AppliedJobPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    serializer_class = TeamAppliedJobDetailSerializer
    model = AppliedJobStatus
    filterset_class = TeamBasedAppliedJobFilter
    ordering = ('-applied_date')
    search_fields = ['applied_by']
    ordering_fields = ['applied_date', 'job__job_posted_date']
    permission_classes = (TeamAppliedJobPermission,)

    # @method_decorator(cache_page(60*2))
    @swagger_auto_schema(responses={200: TeamAppliedJobDetailSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            bd_id_list = Team.objects.get(reporting_to=self.request.user).members.values_list('id', flat=True)
            bd_users = User.objects.filter(id__in=bd_id_list)
            bd_query = UserSerializer(bd_users, many=True)
            job_list = AppliedJobStatus.objects.filter(applied_by__id__in=bd_id_list)
            queryset = self.filter_queryset(job_list)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = self.get_paginated_response(serializer.data)
                data.data['team_members'] = bd_query.data
                end_time = datetime.now()
                start_time = end_time - timedelta(hours=12)
                data.data['last_12_hours_count'] = queryset.filter(applied_date__range=[start_time, end_time]).count()

                return data

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Team.DoesNotExist:
            return Response({"detail": "BD list is empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)
