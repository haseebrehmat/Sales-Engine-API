from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
    lookup_field = 'job'
    permission_classes = (ApplyJobPermission,JobStatusPermission)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job_status = self.request.data.get('status')
        job_id = self.request.data.get('job')

        job_details = JobDetail.objects.get(id=job_id)
        job_details.job_status = job_status
        job_details.save()

        # get current user
        current_user = self.request.user
        if current_user:
            # if current_user and current_user.groups.name=='BD':
            obj = AppliedJobStatus.objects.create(job=job_details, applied_by=current_user)
            obj.save()
            data = JobStatusSerializer(obj, many=False)
            headers = self.get_success_headers(data.data)
            msg = {'detail': 'Job status changed successfully'}
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
        partial = kwargs.pop('partial', False)
        self.kwargs = request.data
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True, request=request)

        job_status = self.request.data.get('status')
        job_id = self.request.data.get('job')

        JobDetail.objects.filter(id=job_id).update(job_status=job_status)
        obj = AppliedJobStatus.objects.get(job_id=job_id)
        data = JobStatusSerializer(obj, many=False)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        msg = {"data": data.data, 'detail': 'Job status updated successfully'}
        return Response(msg, status=status.HTTP_200_OK)
