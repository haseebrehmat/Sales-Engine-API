from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.exceptions import InvalidUserException
from scraper.models import SchedulerSettings, GroupScraper
from scraper.schedulers.job_upload_scheduler import scheduler_settings
from scraper.serializers.scheduler_settings import SchedulerSerializer
from scraper.serializers.group_scraper_scheduler import GroupScraperSerializer
# from settings.celery import restart_server
from settings.utils.helpers import serializer_errors


class GroupScraperView(ListAPIView):
    serializer_class = GroupScraperSerializer

    def get_queryset(self):
        return GroupScraper.objects.all()

    def post(self, request):
        message, is_valid = self.validate_group(request)
        if not is_valid:
            return Response({"detail": message}, status=status.HTTP_406_NOT_ACCEPTABLE)

        data = {
            "time_based": request.data.get("time_based", False),
            "interval_based": request.data.get("interval_based", False),
            "interval": request.data.get("interval", ""),
            "interval_type": request.data.get("interval_type", ""),
            "time": None if request.data.get("time", "") == "" else request.data.get("time"),
            "is_group": True
        }

        name = request.data.get("name", "").lower()

        interval_conditions = [
            request.data.get("interval", "") == "",
            request.data.get("interval_type", "") == ""
        ]
        if request.data.get("interval_based", False) and any(interval_conditions):
            return Response({"detail": "Interval type or interval cannot be empty"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = SchedulerSerializer(data=data)
        if serializer.is_valid():
            scheduler_settings_obj = serializer.create(
                serializer.validated_data)
            GroupScraper.objects.create(
                scheduler_settings=scheduler_settings_obj, name=name)
            data = "Group Scheduler created successfully"
            # scheduler_settings()  # This will update current schedulers
            status_code = status.HTTP_201_CREATED

            return Response({"detail": data}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)

    def validate_group(self, request):
        is_valid = True
        name = request.data.get('name', '').lower()
        group = GroupScraper.objects.filter(name=name).first()
        msg = ''
        if not name:
            is_valid = False
            msg = 'Group name should not be empty.'
        elif group:
            msg = f'Group \'{name}\' already exists'
            is_valid = False
        return msg, is_valid


class GroupScraperDetailView(APIView):
    def get(self, request, pk):
        obj = GroupScraper.objects.filter(pk=pk).first()
        if obj:
            serializer = GroupScraperSerializer(obj, many=False)
            data = serializer.data

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Group Scraper Not Available"}, status=status.HTTP_404_NOT_FOUND)

    # def put(self, request, pk):
    #     queryset = SchedulerSettings.objects.filter(pk=pk).first()
    #     query_dict = request.data.copy()
    #     flag = request.data.get('time_based')
    #     if flag is True:
    #         query_dict['interval'] = None
    #         query_dict['interval_type'] = None
    #     if flag is False:
    #         query_dict['time'] = None
    #     serializer = SchedulerSerializer(queryset, query_dict)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         status_code = status.HTTP_200_OK
    #         message = {"detail": "Scheduler updated successfully"}
    #         scheduler_settings()
    #         return Response(message, status=status_code)
    #
    #     data = serializer_errors(serializer)
    #     raise InvalidUserException(data)
    #

    def delete(self, request, pk):
        group_scraper = GroupScraper.objects.filter(pk=pk).first()
        if group_scraper:
            group_scraper.scheduler_settings.delete()
            group_scraper.delete()
            message = {"detail": "Group Scraper deleted successfully!"}
            status_code = status.HTTP_200_OK
        else:
            message = {"detail": "Group Scraper does not exist!"}
            status_code = status.HTTP_200_OK
        return Response(message, status_code)
