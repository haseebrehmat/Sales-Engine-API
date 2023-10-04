from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from authentication.exceptions import InvalidUserException
from job_portal.serializers.manual_job_upload import ManualJobUploadSerializer
from job_portal.serializers.job_detail import JobDetailSerializer
from settings.utils.helpers import serializer_errors
from rest_framework.permissions import IsAuthenticated
from job_portal.models import JobDetail, JobArchive
from datetime import datetime
import re

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

class ManualJobUploadView(ListAPIView):
    serializer_class = ManualJobUploadSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return JobDetail.objects.filter(is_manual=True)

    def post(self, request):
        conditions = [
            request.data.get("job_title", "") != "",
            request.data.get("company_name", "") != "",
            request.data.get("job_source", "") != "",
            request.data.get("job_type", "") != "",
            request.data.get("address", "") != "",
            request.data.get("job_source_url", "") != "",
            request.data.get("job_posted_date", "") != "",
            request.data.get("tech_keywords", "") != "",
        ]
        if not all(conditions):
            return Response({"detail": "Fields cannot be empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if not ManualJobUploadSerializer.validate_url_field(self, request.data.get("job_source_url", "")):
            return Response({"detail": "Invalid URL"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        data = request.data
        data['tech_stacks'] = data['tech_keywords'].split(',')
        data['job_posted_date'] = str(data['job_posted_date']) + ' ' + str(data['time']) + ':00'
        serializer = ManualJobUploadSerializer(data=data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            data = "Manual Job created successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": data}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)

class ManualJobUploadDetail(APIView):

    def get(self, request, pk):
        query = JobDetail.objects.filter(pk=pk, is_manual=True)
        if query.exists():
            queryset = query.first()
            if queryset.expired_at is None:
                request.data['expired_at'] = datetime.now()
            else:
                request.data['expired_at'] = None
            query.update(**request.data)
            status_code = status.HTTP_200_OK
            message = {"detail": "Job updated successfully"}
            return Response(message, status=status_code)
        else:
            return Response({"detail": "This job does not exist"},
                            status=status.HTTP_404_NOT_FOUND)
