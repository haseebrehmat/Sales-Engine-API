from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from job_scraper.models import SchedulerSync
from job_scraper.schedulers.job_upload_scheduler import load_job_scrappers


class SyncScheduler(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        job_source = request.GET.get("job_source", "all")
        valid_job_sources = [
            "all",
            "linkedin",
            "indeed",
            "dice",
            "careerbuilder",
            "glassdoor",
            "monster",
            "simplyhired",
            "ziprecruiter",
            "adzuna"
        ]
        if job_source.lower() not in valid_job_sources:
            return Response({"detail": f"{job_source} not a valid job source"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        queryset = SchedulerSync.objects.filter(job_source__iexact=job_source.lower()).first()
        if queryset.running:
            message = f"{job_source} sync in progress, Process is already running in the background"
        else:
            message = f"{job_source} sync in progress, It will take a while"
            load_job_scrappers(job_source)

        return Response({"detail": message}, status=status.HTTP_200_OK)


class SchedulerStatusView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = SchedulerSync.objects.all().exclude(job_source=None)
        if len(queryset) is None:
            data = []
        else:
            data = [{"job_source": x.job_source, "running": x.running} for x in queryset]
        return Response(data, status=status.HTTP_200_OK)
