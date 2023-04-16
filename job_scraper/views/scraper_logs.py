from rest_framework.generics import ListAPIView

from job_scraper.models import ScraperLogs
from job_scraper.serializers.scraper_logs_serializer import ScraperLogsSerializer
from job_scraper.utils.custom_pagination import CustomPagination


class ScraperLogView(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = ScraperLogsSerializer
    queryset = ScraperLogs.objects.all()

    def get_queryset(self):
        return self.queryset

