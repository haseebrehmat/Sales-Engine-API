from rest_framework.generics import ListAPIView
from job_portal.models import EditHistory
from job_portal.serializers.detect_changes import EditHistorySerializer
from settings.utils.custom_pagination import CustomPagination


class EditHistoryView(ListAPIView):
    serializer_class = EditHistorySerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return EditHistory.objects.all()
        else:
            return EditHistory.objects.filter(company_id=self.request.user.profile.company_id)


class DetectChangesView(ListAPIView):
    serializer_class = EditHistorySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        conditions = [
            self.request.GET.get("module", "") != "",
            self.request.GET.get("instance_id", "") != ""
        ]
        if all(conditions):
            model = self.request.GET.get("module", "")
            instance_id = self.request.GET.get("instance_id", "")
            data = []
            queryset = EditHistory.objects.filter(company_id=self.request.user.profile.company_id,
                                                  instance_id=instance_id,
                                                  model=model)
            return queryset
        else:
            return EditHistory.objects.none()
