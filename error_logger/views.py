from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import LogSerialzer
from .models import Log

# Create your views here.
class LogsView(ListAPIView):
    serializer_class = LogSerialzer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Log.objects.all()
