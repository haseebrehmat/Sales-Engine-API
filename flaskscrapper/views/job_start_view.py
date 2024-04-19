from scraper.models.group_scraper_query import GroupScraperQuery
from flaskscrapper.models import ScrapersRunningStatus
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from scraper.constants.const import *
from scraper.utils.thread import start_new_thread
from utils.helpers import send_request_to_flask

class JobsStart(APIView):
    permission_classes = (AllowAny,)

    @start_new_thread
    def scraper_start(self, request, job_source, queryset):
        ScrapersRunningStatus.objects.filter(job_source=job_source, running=False).update(running=True)
        while(ScrapersRunningStatus.objects.filter(job_source=job_source, running=True)):
            if ScrapersRunningStatus.objects.filter(job_source=job_source, loop=False):
                json_data = {
                    "source": job_source,
                    "links": [
                        {
                            "job_url": query.link,
                            "job_type": query.job_type
                        }
                        for query in queryset
                    ]
                }
                ScrapersRunningStatus.objects.filter(job_source=job_source, loop=False).update(loop=True)
                send_request_to_flask(json_data)

    def get(self, request, job_source):
        if job_source in SCRAPERS_NAME:
            if not ScrapersRunningStatus.objects.filter(job_source=job_source):
                ScrapersRunningStatus.objects.create(job_source=job_source)
            if ScrapersRunningStatus.objects.filter(job_source=job_source, running=True).update(running=False):
                return Response({"detail": f"{job_source} successfully stopped."}, status.HTTP_200_OK)
            queryset = GroupScraperQuery.objects.filter(job_source=job_source)
            if queryset:
                self.scraper_start(request, job_source, queryset)
                return Response({"detail": f"{job_source} scraper started"}, status.HTTP_200_OK)
            return Response({"detail": f"No link found for {job_source}"}, status.HTTP_404_NOT_FOUND)
        return Response({"detail": "No scraper found with this name"}, status.HTTP_404_NOT_FOUND)
