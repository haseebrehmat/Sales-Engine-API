from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from authentication.exceptions import InvalidUserException
from job_portal.serializers.manual_job_upload import ManualJobUploadSerializer
from settings.utils.helpers import serializer_errors
from rest_framework.permissions import IsAuthenticated

class ManualJobUploadView(ListAPIView):
    serializer_class = ManualJobUploadSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        conditions = [
            request.data.get("job_title", "") != "",
            request.data.get("company_name", "") != "",
            request.data.get("job_source", "") != "",
            request.data.get("job_type", "") != "",
            request.data.get("address", "") != "",
            request.data.get("job_source_url", "") != "",
            request.data.get("job_posted_date", "") != "",
        ]
        if not all(conditions):
            return Response({"detail": "Fields cannot be empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if ManualJobUploadSerializer.validate_url_field(self , request.data.get("job_source_url", "")) == False:
            return Response({"detail": "Invalid URL"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = ManualJobUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            data = "Manual Job created successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": data}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)