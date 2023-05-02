from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from scraper.models import JobSourceQuery
from scraper.serializers.job_source_queries import JobQuerySerializer
from settings.utils.helpers import serializer_errors


class JobQueriesView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = JobSourceQuery.objects.all()
        serializer = JobQuerySerializer(queryset, many=True)
        return Response({"detail": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = JobQuerySerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({"detail": "Settings saved successfully"})
        data = serializer_errors(serializer)
        raise InvalidUserException(data)


class JobQueriesDetailView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        queryset = JobSourceQuery.objects.filter(pk=pk).first()
        serializer = JobQuerySerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = JobSourceQuery.objects.filter(pk=pk).first()
        serializer = JobQuerySerializer(queryset, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Settings updated successfully"})
        data = serializer_errors(serializer)
        raise InvalidUserException(data)



