from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from job_portal.models import BlacklistJobs, JobDetail
from job_portal.serializers.black_list import BlacklistSerializer


class BlackListJobsView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        queryset = BlacklistJobs.objects.filter(company_id=request.user.profile.company.id).first()
        if queryset is not None:
            serializer = BlacklistSerializer(queryset, many=False)
            data = serializer.data
        else:
            data = []
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        check = BlacklistJobs.objects.filter(company_id=request.data.get("company")).update(**request.data)
        if check == 0:
            company_id = request.data.pop("company")
            check = BlacklistJobs.objects.create(**request.data, company_id=company_id)
        if check != 0:
            return Response({"detail": "Settings saved successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Error in saving settings"}, status=status.HTTP_200_OK)


class JobSourcesView(APIView):
    def get(self, request):
        jobs = list(set(JobDetail.objects.all().values_list("company_name", flat=True)))
        return Response({"job_sources": [job for job in jobs if len(job) > 0]})
