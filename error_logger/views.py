from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import LogSerialzer
from .models import Log
from .pagination import LogsPagination
from error_logger.schedulers import run_delete_logs_scheduler

# Create your views here.
class LogsView(ListAPIView):
    serializer_class = LogSerialzer
    permission_classes = (IsAuthenticated,)
    pagination_class = LogsPagination

    def get_queryset(self):
        queryset = Log.objects.all().order_by('-time')
        return self.filter_query(queryset)

    def filter_query(self, queryset):
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(log_message__icontains=search)
        logs_types = self.request.GET.get('logsTypes')
        if logs_types:
            logs_types = logs_types.split(',')
            queryset = queryset.filter(level__in=logs_types) if logs_types else queryset
        request_types = self.request.GET.get('requestTypes')
        if request_types:
            request_types = request_types.split(',')
            queryset = queryset.filter(method__in=request_types) if request_types else queryset
        return queryset


# run_delete_logs_scheduler()
