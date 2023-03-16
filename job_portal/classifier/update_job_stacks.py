from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from job_portal.models import JobDetail


class UpdateJobStackView(APIView):

    def get(self, request):
        if request.user.is_superuser and request.user.is_active:
            jobs = JobDetail.objects.all()
            for job in jobs:
                job.tech_keywords = job.tech_keywords.replace(" / ", "/").lower()
                job.save()
            return Response({"detail": "Job stacks updated successfully"}, status=status.HTTP_200_OK)

        return Response({"detail": "Only SuperAdmin has access to this endpoint"}, status=status.HTTP_400_BAD_REQUEST)
