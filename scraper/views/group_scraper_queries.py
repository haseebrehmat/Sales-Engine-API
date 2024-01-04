import json

from rest_framework import status
from rest_framework import status as s
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F
from django.db.models import Count
from authentication.exceptions import InvalidUserException
from scraper.models import JobSourceQuery, GroupScraperQuery, GroupScraper
#from scraper.schedulers.job_upload_scheduler import start_group_scraper_scheduler
from scraper.serializers.job_source_queries import JobQuerySerializer
from scraper.serializers.group_scraper_queries import GroupScraperQuerySerializer
from settings.utils.helpers import serializer_errors


class GroupScraperQueriesView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        data = {}
        queryset = GroupScraperQuery.objects.exclude(group_scraper=None)
        grouped_record = list(
            queryset.values('group_scraper__name').annotate(total_scraper_jobs=Count('group_scraper__name')))
        grouped_instances = {}
        
        for record in grouped_record:
            group_name = record['group_scraper__name']
            group_objects = {

                             "running_query": [{
                                 "group_scraper": obj.group_scraper.name if obj.group_scraper.name else None,
                                 "link": obj.link if obj.link else None,
                                 "job_type": obj.job_type if obj.job_type else None,
                                 "job_source": obj.job_source if obj.job_source else None,
                                 "status": obj.status if obj.status else None,
                                 "end_time": obj.end_time if obj.end_time else None,
                                 "start_time": obj.start_time if obj.start_time else None
                             } for obj in queryset.filter(group_scraper__name=group_name,
                                                                                      status="running")],
                             "running_count": len(queryset.filter(group_scraper__name=group_name,
                                                                                      status="running")),
                             "remaining_count": len(queryset.filter(group_scraper__name=group_name,
                                                                  status="remaining")),
                             "completed_count": len(queryset.filter(group_scraper__name=group_name,
                                                                    status="completed")),
                             "failed_count": len(queryset.filter(group_scraper__name=group_name,
                                                                    status="failed")),
                             "total_count": len(queryset.filter(group_scraper__name=group_name)),
                             "group_id": GroupScraper.objects.filter(name=group_name).first().id

            }
            data[group_name] = group_objects
        return Response(data, status=status.HTTP_200_OK)



    def post(self, request):
        print(request.data)
        data = []
        group_scraper_id = request.data.get('group_scraper')
        queries = request.data.get('queries')
        for query in queries:
            serializer = GroupScraperQuerySerializer(data=query)
            if serializer.is_valid():
                conditions = [
                    serializer.validated_data.get('link', "") != "",
                    serializer.validated_data.get('job_type', "") != "",
                    serializer.validated_data.get('job_source', "") != ""
                ]
                if not all(conditions):
                    return Response({"detail": "Fields cannot be empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                group_scraper_query = GroupScraperQuery(
                    group_scraper_id=group_scraper_id,
                    link=serializer.validated_data.get('link'),
                    job_type=serializer.validated_data.get('job_type'),
                    job_source=serializer.validated_data.get('job_source')
                )
                data.append(group_scraper_query)
            else:
                data = serializer_errors(serializer)
                raise InvalidUserException(data)
        GroupScraperQuery.objects.bulk_create(data, ignore_conflicts=True)
        return Response({"detail": "Group Scraper Settings saved successfully"})



class GroupScraperQueriesDetailView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        queryset = GroupScraperQuery.objects.filter(pk=pk).first()
        serializer = GroupScraperQuerySerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = GroupScraperQuery.objects.filter(pk=pk).first()
        serializer = GroupScraperQuerySerializer(instance=queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = "Group Query updated successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": message}, status_code)
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
class GroupScraperQueriesStatusWise(APIView):
    def get(self, request):
        group_scraper_id = request.GET.get("group_scraper_id", "")
        status = request.GET.get("status", "")
        if group_scraper_id == "" or status == "":
            return Response({"detail": "Group Scraper Fields should not be empty"})
        group_query = GroupScraper.objects.filter(pk=group_scraper_id)
        queryset = GroupScraperQuery.objects.filter(group_scraper_id=group_scraper_id)
        group_object = {
            "queries": [{
                "id": obj.id,
                "group_scraper": obj.group_scraper.name if obj.group_scraper.name else None,
                "link": obj.link if obj.link else None,
                "job_type": obj.job_type if obj.job_type else None,
                "job_source": obj.job_source if obj.job_source else None,
                "status": obj.status if obj.status else None,
                "end_time": obj.end_time if obj.end_time else None,
                "start_time": obj.start_time if obj.start_time else None
            } for obj in (queryset.filter(status=status) if status != "total" else queryset)],
            "group_id": group_scraper_id if group_query.exists() else None,
            "group_name": group_query.first().name if group_query.exists() else None,
        }
        return Response(group_object, status=s.HTTP_200_OK)






