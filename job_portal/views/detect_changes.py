from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from job_portal.models import EditHistory
from job_portal.serializers.detect_changes import EditHistorySerializer
class EditHistoryView(ListAPIView):
    serializer_class = EditHistorySerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return EditHistory.objects.all()
        else:
            return EditHistory.objects.filter(company_id=self.request.user.profile.company_id)