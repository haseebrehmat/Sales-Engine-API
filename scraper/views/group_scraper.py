from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from scraper.models import GroupScraper, GroupScraperQuery
# from scraper.schedulers.job_upload_scheduler import start_group_scraper_scheduler
from scraper.serializers.group_scraper_scheduler import GroupScraperSerializer
from scraper.serializers.scheduler_settings import SchedulerSerializer
# from settings.celery import restart_server
from settings.utils.helpers import serializer_errors


class GroupScraperView(ListAPIView):
    serializer_class = GroupScraperSerializer
    permission_classes = (AllowAny,)

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
            "is_group": True,
            "week_days": request.data.get('week_days', ""),
            "disabled": request.data.get('disabled', False)
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
            status_code = status.HTTP_201_CREATED
            # start_group_scraper_scheduler()
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
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        obj = GroupScraper.objects.filter(pk=pk).first()
        if obj:
            serializer = GroupScraperSerializer(obj, many=False)
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Group Scraper Not Available"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        obj = GroupScraper.objects.filter(pk=pk).first()
        name = request.data.get('name', '')
        if obj:
            msg, is_valid = self.validate_group(request)
            if obj.name != name.lower() and not is_valid:
                return Response({"detail": msg}, status=status.HTTP_406_NOT_ACCEPTABLE)
            queryset = obj.scheduler_settings
            query_dict = request.data.copy()

            flag = request.data.get('time_based')
            if flag is True:
                time = query_dict['time'] + ":00"
                query_dict['time'] = time
                query_dict['interval'] = None
                query_dict['interval_type'] = None
            if flag is False:
                query_dict['time'] = None
            queryset.week_days = request.data.get("week_days", "")
            serializer = SchedulerSerializer(queryset, query_dict)

            if serializer.is_valid():
                serializer.save()
                obj.disabled = query_dict.get("disabled", obj.disabled)
                if obj.name != name.lower():
                    obj.name = name
                obj.save()
                status_code = status.HTTP_200_OK
                message = {
                    "detail": "Group Scheduler setting updated successfully"}
                # start_group_scraper_scheduler()
                return Response(message, status=status_code)

            data = serializer_errors(serializer)
            raise InvalidUserException(data)
        else:
            return Response({'detail': 'Group scheduler does not exist'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk):
        group_scraper = GroupScraper.objects.filter(pk=pk).first()
        if group_scraper:
            group_scraper_qeury = GroupScraperQuery.objects.filter(
                group_scraper=group_scraper).first()
            if group_scraper_qeury:
                group_scraper_qeury.delete()
            if group_scraper.scheduler_settings:
                group_scraper.scheduler_settings.delete()
            group_scraper.delete()
            message = {"detail": "Group Scraper deleted successfully!"}
            status_code = status.HTTP_200_OK
        else:
            # start_group_scraper_scheduler()
            message = {"detail": "Group Scraper does not exist!"}
            status_code = status.HTTP_200_OK
        return Response(message, status_code)

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


class RunGroupScraper(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({'detail': 'Group Scraper Started'}, status=status.HTTP_200_OK)
