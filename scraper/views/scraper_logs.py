from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from scraper.models import ScraperLogs
from scraper.serializers.scraper_logs_serializer import ScraperLogsSerializer
from scraper.utils.custom_pagination import CustomPagination
import datetime


class ScraperLogView(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = ScraperLogsSerializer
    queryset = ScraperLogs.objects.all().order_by('-updated_at')

    def get_queryset(self):
        params = self.request.query_params
        from_date = params['from_date']
        to_date = params['to_date']

        if from_date:
            from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
            self.queryset = self.queryset.filter(created_at__gte=from_date)

        if to_date:
            to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()
            self.queryset = self.queryset.filter(created_at__lt=to_date + datetime.timedelta(days=1))
        return self.queryset



