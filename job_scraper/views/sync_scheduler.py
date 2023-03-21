from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from job_scraper.models import SchedulerSync
from job_scraper.schedulers.job_upload_scheduler import load_job_scrappers


class SyncScheduler(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        queryset = SchedulerSync.objects.filter(id=1).first()

        if queryset is None:
            message = "Sync in progress, It will take a while"
            SchedulerSync.objects.create(running=True)
            load_job_scrappers()
        elif not queryset.running:
            message = "Sync in progress, It will take a while"
            load_job_scrappers()
        else:
            message = "Sync in progress, Process is already running in the background"
        # return Response({"detail": message}, status=status.HTTP_200_OK)
        return Response({"detail": message}, status=status.HTTP_200_OK)
