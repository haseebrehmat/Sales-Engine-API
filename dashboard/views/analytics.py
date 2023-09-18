import copy
import json
from collections import OrderedDict
from datetime import datetime

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Func, F
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_roles.granting import allof, is_self
from authentication.models import User, Team
from authentication.models.company import Company
from authentication.serializers.company import CompanySerializer
from dashboard.filters.dashboard_analytics import CustomJobFilter
from dashboard.permissions.dashboard import DashboardPermission
from dashboard.serializers.dashboard_anylatics import DashboardAnalyticsSerializer
from job_portal.models import AppliedJobStatus, JobDetail


class DashboardAnalyticsView(ListAPIView):
    expression = Func(F('tech_stacks'), function='unnest')
    keywords = set(
        JobDetail.objects.only('tech_stacks').annotate(keywords=expression).values_list('keywords', flat=True))
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
    permission_classes = (DashboardPermission,)

    @swagger_auto_schema(responses={200: DashboardAnalyticsSerializer(many=False)})
    def get(self, request, *args, **kwargs):
        from_date = request.GET.get("from_date", "")
        to_date = request.GET.get("to_date", "")
        request.GET._mutable = True

        if from_date != "":
            from_date = from_date + " 00:00:00"
            from_date = datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S")
            request.GET["from_date"] = from_date
        if to_date != "":
            to_date = to_date + " 23:59:59"
            to_date = datetime.strptime(to_date, "%Y-%m-%d %H:%M:%S")
            request.GET["to_date"] = to_date

        return self.list(request, *args, **kwargs)

    def keyword_count(self):
        unique_keyword_object = []
        for x in self.keywords:
            unique_keyword_object.append(
                {
                    'name': x,
                    'value': JobDetail.objects.filter(tech_stacks__contains=[x]).count()
                }
            )

        return sorted(unique_keyword_object, key=lambda x: x['value'], reverse=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            company = request.user.profile.company.id
        except:
            company = request.GET.get("company", "")
            if company == 'undefined':
                company = ''

        # get all users under the current user team
        if request.user.is_superuser and not company:
            company = Company.objects.filter(status=True)
            teams = Team.objects.filter(reporting_to__profile__company_id__in=company)
        else:
            teams = Team.objects.filter(reporting_to__profile__company_id=company)

        user_team = teams.values_list('members__id', flat=True)

        # get all statistics
        queryset = queryset.filter(applied_by__in=user_team)

        job_status_counts = queryset.values('job_status').annotate(count=Count('job_status'))
        unique_count_dic = json.dumps(list(job_status_counts), cls=DjangoJSONEncoder)
        status_count_data = json.loads(unique_count_dic)
        status_count_dic = self.map_status(status_count_data)
        status_count_dic['total'] = len(queryset)
        status_count_dic = [{'name': i[0], 'value': i[1]} for i in status_count_dic.items()]

        # without pagination
        unique_users = list(set(queryset.values_list('applied_by__id')))
        unique_users_list = []
        for item in list(unique_users):
            data = []
            if queryset.count() > 0:
                data = queryset.filter(applied_by=item).values('job_status').annotate(
                    count=Count('job_status'))
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
        # serializer = self.get_serializer(queryset, many=False)
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
            6: 'hot',
            7: 'prospects'
        }
        for i in status_count_data:
            if i['job_status'] in job_status_keys:
                result_data[job_status_keys[i['job_status']]] += i['count']
        result_data['total'] = len(status_count_data)
        return copy.deepcopy(result_data)
