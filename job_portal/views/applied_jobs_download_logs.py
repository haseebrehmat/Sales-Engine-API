from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from job_portal.models import DownloadLogs, AppliedJobStatus, JobDetail
from job_portal.serializers.download_logs import DownloadLogsSerializer
from settings.utils.custom_pagination import CustomPagination


class AppliedJobDownloadsView(ListAPIView):
    permission_classes = (AllowAny, )
    queryset = DownloadLogs.objects.all().order_by('-created_at')
    serializer_class = DownloadLogsSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        qs = self.queryset.filter(user=self.request.user)
        return qs


class FilterView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        job_sources = set(JobDetail.objects.only('job_source').values_list('job_source', flat=True))
        tech_keywords = set(JobDetail.objects.only('tech_keywords').values_list('tech_keywords', flat=True))
        return Response({'job_sources': job_sources, 'tech_keywords': tech_keywords}, status=200)
