import re
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.exceptions import InvalidUserException
from scraper.models import JobSource
from scraper.serializers.job_sources import JobSourceSerializer
from settings.utils.helpers import serializer_errors

class JobSourceView(ListAPIView):
    serializer_class = JobSourceSerializer
    def get_queryset(self):
        return JobSource.objects.all()

    def post(self, request):
        pattern = r'^[a-zA-Z_]+$'
        conditions = [
            request.data.get("name", "") != "",
            request.data.get("key", "") != "",
        ]
        if re.match(pattern, request.data.get("key")) is None:
            return Response({"detail": "Key only allows underscore without space"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        if all(conditions):
            serializer = JobSourceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.create(serializer.validated_data)
                data = "Job source created successfuly"
                status_code = status.HTTP_201_CREATED
                return Response({"detail": data}, status_code)
            else:
                data = serializer_errors(serializer)
                raise InvalidUserException(data)
        else:
            return Response({"detail": "Feilds cannot be empty"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
class JobSourceDetailView(APIView):
    def get(self, request, pk):
        obj = JobSource.objects.filter(pk=pk).first()
        if obj:
            serializer = JobSourceSerializer(obj, many=False)
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Job source not available"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        pattern = r'^[a-zA-Z_]+$'
        conditions = [
            request.data.get("name", "") != "",
            request.data.get("key", "") != ""
        ]
        if re.match(pattern, request.data.get("key")) is None:
            return Response({"detail": "Key only allows underscore without space"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        if all(conditions):
            queryset = JobSource.objects.filter(pk=pk).first()
            serializer = JobSourceSerializer(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                status_code = status.HTTP_200_OK
                message = {"detail": "Job source updated successfully"}
                return Response(message, status=status_code)

            data = serializer_errors(serializer)
            raise InvalidUserException(data)
        else:
            return Response({"detail": "Feilds cannot be empty"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk):
        JobSource.objects.filter(pk=pk).delete()
        message = {"detail": "Job source deleted successfully"}
        return Response(message, status=status.HTTP_200_OK)
