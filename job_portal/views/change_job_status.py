from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.models import Team
from job_portal.exceptions import NoActiveUserException
from job_portal.models import AppliedJobStatus, JobDetail
from job_portal.permissions.applied_job_status import ApplyJobPermission
from job_portal.permissions.change_job import JobStatusPermission
from job_portal.serializers.applied_job import JobStatusSerializer
from settings.utils.helpers import is_valid_uuid


class ChangeJobStatusView(CreateAPIView, UpdateAPIView):
    serializer_class = JobStatusSerializer
    queryset = AppliedJobStatus.objects.all()
    http_method_names = ['post', 'patch']
    lookup_field = 'id'
    permission_classes = [ApplyJobPermission|JobStatusPermission,]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job_status = self.request.data.get('status')
        job_id = self.request.data.get('job')

        job_details = JobDetail.objects.get(id=job_id)
        # get current user
        current_user = self.request.user
        if current_user:
            # make sure the current user apply only one time on one job
            obj,create = AppliedJobStatus.objects.get_or_create(job=job_details, applied_by=current_user)
            if not create:
                return Response({'detail':'User already applied on this job'}, status=status.HTTP_400_BAD_REQUEST,)
            obj.save()
            data = JobStatusSerializer(obj, many=False)
            headers = self.get_success_headers(data.data)
            msg = {'detail': 'Job applied successfully'}
            return Response(msg, status=status.HTTP_200_OK, headers=headers)
        else:
            raise NoActiveUserException(detail=f'No active user found')

    def post(self, request, *args, **kwargs):
        job_id = request.data.get('job', False)
        if is_valid_uuid(job_id):
            result = JobDetail.objects.filter(pk=job_id)
            if result.count() > 0:
                return self.create(request, *args, **kwargs)
            else:
                msg = {'detail': f'No such job exist with id {job_id}'}
                return Response(msg, status=status.HTTP_404_NOT_FOUND)
        else:
            error = f'{job_id} is not a valid job ID' if job_id else "ID not found"
            msg = {'detail': error}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        self.kwargs = request.data
        job_status = self.request.data.get('status',None)
        id = self.request.data.get('id',None)
        obj = AppliedJobStatus.objects.get(id=id)

        instance = self.get_queryset().filter(id=self.kwargs.get('job',''))
        # current use must be the lead
        user_team = Team.objects.filter(reporting_to=request.user,members=obj.applied_by)
        if len(user_team) == 0:
            msg = {'detail': 'User is not a part of the current user team'}
            return Response(msg, status=status.HTTP_200_OK)

        if len(instance) != 0:
            instance.update(job_status=job_status)
            data = JobStatusSerializer(obj, many=False)

            msg = {"data": data.data, 'detail': 'Job status updated successfully'}
            return Response(msg, status=status.HTTP_200_OK)
        else:
            msg = {'detail': 'Applied job id not found'}
            return Response(msg, status=status.HTTP_200_OK)
