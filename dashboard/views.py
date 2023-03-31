import copy
import json
from collections import OrderedDict

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.models import User
from dashboard.filters.dashboard_analytics import CustomJobFilter
from dashboard.serializers.dashboard_anylatics import DashboardAnalyticsSerializer
from job_portal.models import AppliedJobStatus, JobDetail


class DashboardAnalyticsView(ListAPIView):
    queryset = AppliedJobStatus.objects.all()
    serializer_class = DashboardAnalyticsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    model = AppliedJobStatus
    parser_classes = (MultiPartParser, JSONParser)
    filterset_class = CustomJobFilter
    ordering = ('-applied_date')
    search_fields = ['applied_by']
    http_method_names = ['get']
    ordering_fields = ['job__job_posted_date', 'applied_date']
    permission_classes = (AllowAny,)

    @swagger_auto_schema(responses={200: DashboardAnalyticsSerializer(many=False)})
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def keyword_count(self):
        unique_keyword_object = JobDetail.objects.extra(select={'name': 'tech_keywords'}).values('name').annotate(
            value=Count('tech_keywords'))
        unique_count_dic = json.dumps(list(unique_keyword_object), cls=DjangoJSONEncoder)
        unique_count_data = json.loads(unique_count_dic)
        return sorted(unique_count_data, key=lambda x: x["value"], reverse=True)

    # @method_decorator(cache_page(60*2))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # get all statistics
        job_status_counts = queryset.values('job__job_status').annotate(count=Count('job__job_status'))
        unique_count_dic = json.dumps(list(job_status_counts), cls=DjangoJSONEncoder)
        status_count_data = json.loads(unique_count_dic)
        status_count_dic = self.map_status(status_count_data)
        status_count_dic = [{'name': i[0], 'value': i[1]} for i in status_count_dic.items()]

        # without pagination
        unique_users = list(set(AppliedJobStatus.objects.all().values_list('applied_by__id')))
        unique_users_list = []
        for item in list(unique_users):
            data = []
            if queryset.count() > 0:
                data = queryset.filter(applied_by=item).values('job__job_status').annotate(
                    count=Count('job__job_status'))
            user_count_dic = json.dumps(list(data), cls=DjangoJSONEncoder)
            user_status_count_data = json.loads(user_count_dic)
            user_status_count_dic = self.map_status(user_status_count_data)
            # get userdata

            user_object = User.objects.get(id=str(item[0]))
            user_status_count_dic['name'] = user_object.username
            user_status_count_dic['id'] = user_object.id
            unique_users_list.append(copy.deepcopy(user_status_count_dic))

        final_dictionary = {
            'statistics': status_count_dic,
            'leads': unique_users_list,
            'tech_keywords_count_list': self.keyword_count(),
            'weekly_leads': []
        }
        serializer = self.get_serializer(queryset, many=False)
        return Response(final_dictionary)

    def map_status(self, status_count_data):
        result_data = OrderedDict({
            'total': 0,
            'prospects': 0,
            'cold': 0,
            'warm': 0,
            'hot': 0,
            'rejected': 0,
            'hired': 0,
        })
        job_status_keys = {
            2: 'hired',
            3: 'rejected',
            4: 'cold',
            5: 'warm',
            6: 'hot'
        }
        for i in status_count_data:
            if i['job__job_status'] in job_status_keys:
                result_data[job_status_keys[i['job__job_status']]] += i['count']
                # data[job_status_keys[i['job__job_status']]] = i['count']
        # calculate total, prospects

        result_data['total'] = len(status_count_data)
        # result_data['prospects'] = (result_data['total']) - (result_data['hired']+result_data['rejected']+result_data['cold'] + result_data['warm'] + result_data['rejected'])
        return copy.deepcopy(result_data)
        # return result_data
