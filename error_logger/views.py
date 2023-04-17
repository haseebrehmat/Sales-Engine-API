from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import LogSerialzer
from .models import Log
from .pagination import LogsPagination

# Create your views here.
class LogsView(ListAPIView):
    serializer_class = LogSerialzer
    permission_classes = ()
    pagination_class = LogsPagination
    def get_queryset(self):
        return Log.objects.all().order_by('-time')
