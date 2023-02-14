import uuid
from threading import Thread
from django_filters.rest_framework import DjangoFilterBackend

from authentication.models import User
from authentication.models.team_management import TeamManagement
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema
from rest_framework import pagination, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authentication.serializers.users import  UserSerializer
from job_portal.classifier.job_classifier import JobClassifier
from job_portal.data_parser.job_parser import JobParser
from job_portal.exceptions import InvalidFileException, NotAuthorized
from job_portal.filters.applied_job import CustomAppliedJobFilter, TeamBasedAppliedJobFilter
from job_portal.filters.job_detail import CustomJobFilter
from job_portal.models import AppliedJobStatus, JobDetail
from job_portal.pagination.applied_job import AppliedJobPagination
from job_portal.pagination.job_detail import CustomPagination
from job_portal.serializers.applied_job import AppliedJobDetailSerializer, JobStatusSerializer, \
    TeamAppliedJobDetailSerializer
from job_portal.serializers.job_detail import JobDetailOutputSerializer, JobDetailSerializer, JobDataUploadSerializer


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


class JobDetailsView(ModelViewSet):
    queryset = JobDetail.objects.all()
    serializer_class = JobDetailSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    model = JobDetail
    parser_classes = (MultiPartParser, JSONParser)
    pagination_class = CustomPagination
    filterset_class = CustomJobFilter
    ordering = ('-job_posted_date')
    search_fields = ['job_title', 'job_description']
    http_method_names = ['get']
    ordering_fields = ['job_title', 'job_type','job_posted_date','company_name']

    @method_decorator(cache_page(60*2))
    @swagger_auto_schema(responses={200: JobDetailOutputSerializer(many=False)})
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ChangeJobStatusView(CreateAPIView,UpdateAPIView):
    serializer_class = JobStatusSerializer()
    queryset = AppliedJobStatus.objects.all()
    http_method_names = ['post','patch']
    lookup_field = 'job'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        msg = {"msg":"Job status changed successfully",'details':'Job status changed successfully'}
        return Response(msg, status=status.HTTP_200_OK, headers=headers)



    def post(self, request, *args, **kwargs):
        job_id = request.data['job']
        if is_valid_uuid(job_id):
            result = JobDetail.objects.filter(pk=job_id)
            if result.count() > 0:
                return self.create(request, *args, **kwargs)
            else:
                msg = {"msg": "Invalid Job", 'details': f'No such job exist with id {job_id}'}
                return Response(msg, status=status.HTTP_404_NOT_FOUND)
        else:
            msg = {"msg": "Invalid Job ID",
                   'details': f'{job_id} is not a valid job ID'}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        self.kwargs = request.data
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True,request=request)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        msg = {"data":serializer.data,"msg": "Job status updated successfully", 'details': 'Job status updated successfully'}
        return Response(msg, status=status.HTTP_200_OK)



class AppliedJobDetailsView(ListAPIView):
    queryset = AppliedJobStatus.objects.all()
    pagination_class = AppliedJobPagination
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    serializer_class = AppliedJobDetailSerializer
    model = AppliedJobStatus
    filterset_class = CustomAppliedJobFilter
    ordering = ('-job_id__job_posted_date')
    search_fields = ['job__job_title', 'job__job_description','job__tech_keywords', 'job__job_type']
    ordering_fields = ['job__tech_keywords', 'job__job_type', 'job__job_posted_date']

    # @method_decorator(cache_page(60*2))
    @swagger_auto_schema(responses={200: AppliedJobDetailSerializer(many=False)})
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class JobDataUploadView(CreateAPIView):
    serializer_class = JobDataUploadSerializer

    def post(self, request, *args, **kwargs):
        job_file = request.FILES.getlist('file_upload',[])

        job_parser = JobParser(job_file)
        # validate files first
        is_valid,message = job_parser.validate_file()
        if not is_valid:
            raise InvalidFileException(detail=message)

        job_parser.parse_file()
        thread = Thread(target=self.upload_file,args=(job_parser,),)
        thread.start()
        return Response({"msg":"data uploaded successfully",'details':'data uploaded successfully'},status=200)


    def upload_file(self,job_parser):
        # parse, classify and upload data to database
        classify_data = JobClassifier(job_parser.data_frame)
        classify_data.classify()

        model_instances = [
            JobDetail(
                job_title=job_item.job_title,
                company_name=job_item.company_name,
                job_source=job_item.job_source,
                job_type=job_item.job_type,
                address=job_item.address,
                job_description=job_item.job_description,
                tech_keywords=job_item.tech_keywords,
                job_posted_date=job_item.job_posted_date,
                job_source_url=job_item.job_source_url,
            ) for job_item in classify_data.data_frame.itertuples()]

        JobDetail.objects.bulk_create(model_instances, ignore_conflicts=True,batch_size=1000)



class ListAppliedJobView(ListAPIView):
    queryset = AppliedJobStatus.objects.all()
    pagination_class = AppliedJobPagination
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    serializer_class = TeamAppliedJobDetailSerializer
    model = AppliedJobStatus
    filterset_class = TeamBasedAppliedJobFilter
    ordering = ('-applied_date')
    search_fields = ['applied_by']
    ordering_fields = ['applied_date', 'job__job_posted_date']

    # @method_decorator(cache_page(60*2))
    @swagger_auto_schema(responses={200: TeamAppliedJobDetailSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        # check for the roles here
        user_role_id = None
        roles_list = self.request.user.groups.values_list('id', flat=True)

        if roles_list.count() > 0:
            user_role_id =  roles_list[0]
            group_role = Group.objects.get(id=user_role_id)
            if group_role.name == 'TL':

                bd_id_list = TeamManagement.objects.get(user_id = self.request.user).reporting.values_list('id',flat=True)
                bd_users  = User.objects.filter(id__in=bd_id_list)
                bd_query = UserSerializer(bd_users,many=True)


                job_list = AppliedJobStatus.objects.filter(applied_by__id__in=bd_id_list)
                query_ = job_list
                queryset = self.filter_queryset(query_)
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    data = self.get_paginated_response(serializer.data)
                    data.data['team_memmbers'] = bd_query.data
                    return data


                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            else:
                raise NotAuthorized(detail=f"User does not have any roles defined")
        else:
            raise NotAuthorized(detail=f"User cannot access the data with role")