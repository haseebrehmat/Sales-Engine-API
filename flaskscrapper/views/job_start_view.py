from scraper.models.group_scraper_query import GroupScraperQuery
from flaskscrapper.models import ScraperRunningStatus, ScrapersLoopStatus
from rest_framework.permissions import AllowAny
from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from scraper.constants.const import *
from scraper.utils.thread import start_new_thread
from django.core.serializers.json import DjangoJSONEncoder
import json

from utils.helpers import send_request_to_flask

class JobsStart(APIView):
    permission_classes = (AllowAny,)

    @start_new_thread
    def scraper_start(self, request, job_source, queryset):
        ScraperRunningStatus.objects.filter(job_source=job_source, status=False).update(status=True)
        while(ScraperRunningStatus.objects.filter(job_source=job_source, status=True)):
            if not ScrapersLoopStatus.objects.filter(job_source=job_source):
                ScrapersLoopStatus.objects.create(job_source=job_source)
            if ScrapersLoopStatus.objects.filter(job_source=job_source, loop_status=False):
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
                ScrapersLoopStatus.objects.filter(job_source=job_source, loop_status=False).update(loop_status=True)
                send_request_to_flask(json_data)

    def get(self, request, job_source):
        if job_source in SCRAPERS_NAME:
            if not ScraperRunningStatus.objects.filter(job_source=job_source):
                ScraperRunningStatus.objects.create(job_source=job_source)
            if ScraperRunningStatus.objects.filter(job_source=job_source, status=True).update(status=False):
                return Response({"detail": f"{job_source} successfully stopped."}, status.HTTP_200_OK)
            scraper_exists = ScraperRunningStatus.objects.filter(job_source=job_source, status=False)
            if scraper_exists:
                queryset = GroupScraperQuery.objects.filter(job_source=job_source)
                if queryset:
                    self.scraper_start(request, job_source, queryset)
                    return Response({"detail": f"{job_source} scraper started"}, status.HTTP_200_OK)
                return Response({"detail": f"No link found for {job_source}"}, status.HTTP_404_NOT_FOUND)
            return Response({"detail": "This scraper is already running"}, status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "No scraper found with this name"}, status.HTTP_404_NOT_FOUND)
