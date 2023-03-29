from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from job_scraper.models import SchedulerSync
from job_scraper.schedulers.job_upload_scheduler import load_job_scrappers


class SyncScheduler(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        job_source = request.GET.get("job_source", "all")

        try:
            queryset = SchedulerSync.objects.get(job_source=job_source)
        except SchedulerSync.DoesNotExist:
            queryset = SchedulerSync.objects.create(running=False, job_source=job_source)

        if queryset.running:
            message = "Sync in progress, Process is already running in the background"
        else:
            message = "Sync in progress, It will take a while"
            load_job_scrappers(job_source)

        return Response({"detail": message}, status=status.HTTP_200_OK)
