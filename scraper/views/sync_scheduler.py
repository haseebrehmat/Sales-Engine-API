from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from time import sleep
from scraper.models import SchedulerSync
from scraper.models import AllSyncConfig
from scraper.utils.scraper_permission import ScraperPermissions
from scraper.schedulers.job_upload_scheduler import load_job_scrappers, load_all_job_scrappers


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
            "adzuna",
            "googlecareers"
        ]
        if job_source.lower() not in valid_job_sources:
            return Response({"detail": f"{job_source} not a valid job source"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        queryset = SchedulerSync.objects.filter(job_source__iexact=job_source.lower())

        for x in queryset:
            if x.type == 'time/interval' and x.running:
                message = f"Cannot start {job_source} instant scraper, Time/Interval based already running"
                return Response({"detail": message}, status=status.HTTP_200_OK)
        queryset = queryset.filter(type="instant").first()
        if queryset.running:
            message = f"{job_source} sync in progress, Process is already running in the background"
        else:
            message = f"{job_source} sync in progress, It will take a while"
            load_job_scrappers(job_source)  # running on separate thread

        return Response({"detail": message}, status=status.HTTP_200_OK)


class SyncAllScrapersView(APIView):
    permission_classes = (ScraperPermissions,)

    def post(self, request):
        if AllSyncConfig.objects.count() == 0:
            AllSyncConfig.objects.create(status=False)
        sync_status = bool(AllSyncConfig.objects.all().first().status)
        if sync_status:
            AllSyncConfig.objects.all().update(status=False)
        else:
            AllSyncConfig.objects.all().update(status=True)
            load_all_job_scrappers()
        if sync_status:
            return Response({"Sync stopped"}, status=status.HTTP_200_OK)
        else:
            return Response({"Sync started"}, status=status.HTTP_200_OK)

    def get(self, request):
        if AllSyncConfig.objects.filter(status=True).first() is not None:
            return Response(True)
        return Response(False)


class SchedulerStatusView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = SchedulerSync.objects.exclude(job_source=None)
        if len(queryset) is None:
            data = []
        else:
            data = [{"job_source": x.job_source, "running": x.running, "type": x.type} for x in queryset]
        return Response(data, status=status.HTTP_200_OK)
