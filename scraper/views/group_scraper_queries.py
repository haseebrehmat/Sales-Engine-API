from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from scraper.models import JobSourceQuery, GroupScraperQuery
from scraper.serializers.job_source_queries import JobQuerySerializer
from scraper.serializers.group_scraper_queries import GroupScraperQuerySerializer
from settings.utils.helpers import serializer_errors


class GroupScraperQueriesView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, group_id):
        queryset = GroupScraperQuery.objects.filter(group_scraper_id=group_id)
        serializer = GroupScraperQuerySerializer(queryset, many=True)
        return Response({"detail": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GroupScraperQuerySerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({"detail": "Group Scraper Settings saved successfully"})
        data = serializer_errors(serializer)
        raise InvalidUserException(data)


class GroupScraperQueriesDetailView(APIView):
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
