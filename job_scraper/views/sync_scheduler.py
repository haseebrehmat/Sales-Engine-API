from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from job_scraper.models import SchedulerSync
from job_scraper.schedulers.job_upload_scheduler import load_job_scrappers


class SyncScheduler(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        queryset = SchedulerSync.objects.filter(running=True).first()

        if queryset is not None and queryset.running:
            message = "Sync in progress, Process is already running in the background"

        else:
            message = "Sync in progress, It will take a while"
            if queryset is None:
                SchedulerSync.objects.create(running=True)
            load_job_scrappers()

        return Response({"detail": message}, status=status.HTTP_200_OK)
