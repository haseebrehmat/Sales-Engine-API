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

    def get(self, request):
        queryset = GroupScraperQuery.objects.all()
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
        queryset = GroupScraperQuery.objects.filter(pk=pk).first()
        serializer = GroupScraperQuerySerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = GroupScraperQuery.objects.filter(pk=pk).first()
        serializer = GroupScraperQuerySerializer(queryset, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Group scraper query updated successfully"})
        data = serializer_errors(serializer)
        raise InvalidUserException(data)

    def delete(self, request, pk):
        queryset = GroupScraperQuery.objects.filter(pk=pk).first()
        if queryset:
            queryset.delete()
            msg = 'Group Scraper Query delete successfully!'
            status_code = status.HTTP_200_OK
        else:
            msg = 'Group Scraper Query does not exist!'
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response({"detail": msg}, status=status_code)
