from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.exceptions import InvalidUserException
from scraper.models import SchedulerSettings
from scraper.schedulers.job_upload_scheduler import scheduler_settings
from scraper.serializers.scheduler_settings import SchedulerSerializer
# from settings.celery import restart_server
from settings.utils.helpers import serializer_errors


class SchedulerView(ListAPIView):
    serializer_class = SchedulerSerializer

    def get_queryset(self):
        return SchedulerSettings.objects.filter(is_group=False)

    def post(self, request):
        message, is_valid = self.validate_job_source(request)
        if not is_valid:
            return Response({"detail": message}, status=status.HTTP_406_NOT_ACCEPTABLE)

        data = {
            "time_based": request.data.get("time_based", False),
            "interval_based": request.data.get("interval_based", False),
            "interval": request.data.get("interval", ""),
            "interval_type": request.data.get("interval_type", ""),
            "time": None if request.data.get("time", "") == "" else request.data.get("time"),
            "job_source": request.data.get("job_source", "")
        }
        interval_conditions = [
            request.data.get("interval", "") == "",
            request.data.get("interval_type", "") == ""
        ]
        if request.data.get("interval_based", False) and any(interval_conditions):
            return Response({"detail": "Interval type or interval cannot be empty"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = SchedulerSerializer(data=data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            data = "Scheduler created successfully"
            status_code = status.HTTP_201_CREATED

            return Response({"detail": data}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)

    def validate_job_source(self, request):
        is_valid = True
        message = ""
        my_dict = {
            'linkedin': 'Linkedin',
            'careerbuilder': 'Career Builder',
            'adzuna': 'Adzuna',
            'dice': 'Dice',
            'indeed': 'Indeed',
            'ziprecruiter': 'Zip Recruiter',
            'glassdoor': 'Glassdoor',
            'monster': 'Monster',
            'simplyhired': 'Simply Hired',
            'googlecareers': 'Google Careers',
            'jooble': 'Jooble',
            'talent': 'Talent',
            'careerjet': 'CareerJet',
            'rubynow': 'Ruby Now' ,
            'hirenovice': 'Hire Novice',
            'remoteco': 'Remote CO'
        }

        if request.data.get('job_source') not in my_dict:
            message = "Job Source is not acceptable"
            is_valid = False
        return message, is_valid


class SchedulerDetailView(APIView):
    def get(self, request, pk):
        obj = SchedulerSettings.objects.filter(pk=pk).first()
        if obj:
            serializer = SchedulerSerializer(obj, many=False)
            data = serializer.data

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Scheduler Not Available"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        queryset = SchedulerSettings.objects.filter(pk=pk).first()
        query_dict = request.data.copy()
        flag = request.data.get('time_based')
        if flag is True:
            query_dict['interval'] = None
            query_dict['interval_type'] = None
        if flag is False:
            query_dict['time'] = None
        serializer = SchedulerSerializer(queryset, query_dict)

        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_200_OK
            message = {"detail": "Scheduler updated successfully"}
            return Response(message, status=status_code)

        data = serializer_errors(serializer)
        raise InvalidUserException(data)

    def delete(self, request, pk):
        SchedulerSettings.objects.filter(pk=pk).delete()
        message = {"detail": "Scheduler deleted successfully"}
        return Response(message, status=status.HTTP_200_OK)
