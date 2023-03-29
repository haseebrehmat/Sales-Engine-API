from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from job_scraper.models import SchedulerSync
from job_scraper.schedulers.job_upload_scheduler import load_job_scrappers


class SyncScheduler(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        queryset = SchedulerSync.objects.filter().first()
        if queryset is None:
            try:
                SchedulerSync.objects.all().delete()    # incase if there is any entry exists
                queryset = SchedulerSync.objects.create(running=False)
            except Exception as e:
                print(e)
                load_job_scrappers()
        if queryset.running:
            message = "Sync in progress, Process is already running in the background"
        else:
            message = "Sync in progress, It will take a while"
            load_job_scrappers()

        return Response({"detail": message}, status=status.HTTP_200_OK)
