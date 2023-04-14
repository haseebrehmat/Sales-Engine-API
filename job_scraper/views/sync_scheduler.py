from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from time import sleep
from job_scraper.models import SchedulerSync
from job_scraper.models import AllSyncConfig
from job_scraper.utils.scraper_permission import ScraperPermissions
from job_scraper.schedulers.job_upload_scheduler import load_job_scrappers, load_all_job_scrappers


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
            load_job_scrappers.delay(job_source)  # running on celery shared task

        return Response({"detail": message}, status=status.HTTP_200_OK)


class SyncAllScrapersView(APIView):
    permission_classes = (ScraperPermissions,)

    def post(self, request):
        sync_status = bool(AllSyncConfig.objects.all().first().status)
        queryset = AllSyncConfig.objects.all()
        if queryset.count() > 0:
            if sync_status:
                AllSyncConfig.objects.all().update(status=False)
            else:
                AllSyncConfig.objects.all().update(status=True)
                load_all_job_scrappers()
        else:
            if sync_status:
                AllSyncConfig.objects.create(status=False)
            else:
                AllSyncConfig.objects.create(status=True)
                load_all_job_scrappers()
        if sync_status:
            return Response({"Sync stopped"}, status=status.HTTP_200_OK)
        else:
            return Response({"Sync started"}, status=status.HTTP_200_OK)

    def get(self, request):
        if bool(AllSyncConfig.objects.filter(status=True).values_list(flat=True)):
            return Response(True)
        return Response(False)


class SchedulerStatusView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = SchedulerSync.objects.all().exclude(job_source=None)
        if len(queryset) is None:
            data = []
        else:
            data = [{"job_source": x.job_source, "running": x.running} for x in queryset]
        return Response(data, status=status.HTTP_200_OK)
