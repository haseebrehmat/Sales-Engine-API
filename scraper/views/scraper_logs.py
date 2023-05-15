from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from scraper.models import ScraperLogs
from scraper.serializers.scraper_logs_serializer import ScraperLogsSerializer
from scraper.utils.custom_pagination import CustomPagination


class ScraperLogView(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = ScraperLogsSerializer
    queryset = ScraperLogs.objects.all().order_by('-updated_at')

    def get_queryset(self):
        return self.queryset

