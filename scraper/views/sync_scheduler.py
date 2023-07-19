from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from time import sleep
from scraper.models import SchedulerSync
from scraper.models import AllSyncConfig
from scraper.utils.scraper_permission import ScraperPermissions
from scraper.schedulers.job_upload_scheduler import load_job_scrappers, load_all_job_scrappers


def run_scrapers_manually(job_source='all'):
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
            "googlecareers",
            "jooble",
            "talent",
            "careerjet",
            "dailyremote"
        ]
    if job_source.lower() not in valid_job_sources:
        return {"detail": f"{job_source} not a valid job source"}, status.HTTP_406_NOT_ACCEPTABLE

    queryset = SchedulerSync.objects.filter(job_source__iexact=job_source.lower())

    for x in queryset:
        if x.type == 'time/interval' and x.running:
            message = f"Cannot start {job_source} instant scraper, Time/Interval based already running"
            return {"detail": message}, status.HTTP_200_OK
    queryset = queryset.filter(type="instant").first()
    if queryset:
        if queryset.running:
            message = f"{job_source} sync in progress, Process is already running in the background"
        else:
            message = f"{job_source} sync in progress, It will take a while"
            load_job_scrappers(job_source)  # running on separate thread
            return {"detail": message}, status.HTTP_200_OK
    else:
        return {"detail": f'Scheduler setting is missing for {job_source}.'}, status.HTTP_400_BAD_REQUEST


class SyncScheduler(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            job_source = request.GET.get("job_source", "all")
            data, status_code = run_scrapers_manually(job_source) # running on separate thread
            return Response(data, status_code)
        except Exception as e:
            return Response(str(e), 400)


class SyncAllScrapersView(APIView):
    permission_classes = (ScraperPermissions,)

    def post(self, request):
        if AllSyncConfig.objects.count() == 0:
            AllSyncConfig.objects.create(status=False)
        sync_status = bool(AllSyncConfig.objects.all().first().status)
        if sync_status:
            AllSyncConfig.objects.all().update(status=False)
            return Response({"Sync stopped"}, status=status.HTTP_200_OK)
        else:
            AllSyncConfig.objects.all().update(status=True)
            load_all_job_scrappers()
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
        infinite_scraper_running_status = False
        if AllSyncConfig.objects.filter(status=True).first() is not None:
            infinite_scraper_running_status = True
        data.append({"job_source": 'all', "running": infinite_scraper_running_status, "type": 'Infinite Scrapper'})
        try:
            from scraper.schedulers.job_upload_scheduler import current_scraper
            data.append({"job_source": current_scraper, "running": True if current_scraper else False, "type": 'Group Scraper'})
        except Exception as e:
            print(e)
        return Response(data, status=status.HTTP_200_OK)
