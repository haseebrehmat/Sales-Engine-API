from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from xhtml2pdf import pisa

from authentication.models import Team
from job_portal.exceptions import NoActiveUserException
from job_portal.models import AppliedJobStatus, JobDetail
from job_portal.permissions.applied_job_status import ApplyJobPermission
from job_portal.permissions.change_job import JobStatusPermission
from job_portal.serializers.applied_job import JobStatusSerializer
from settings.utils.helpers import is_valid_uuid
from utils.upload_to_s3 import upload_pdf


class ChangeJobStatusView(CreateAPIView, UpdateAPIView):
    serializer_class = JobStatusSerializer
    queryset = AppliedJobStatus.objects.all()
    http_method_names = ['post', 'patch']
    lookup_field = 'id'
    permission_classes = [ApplyJobPermission | JobStatusPermission, ]

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        vertical_id = request.data.get("vertical_id", "")
        resume = request.data.pop("resume", None)
        cover_letter = request.data.pop("cover_letter", None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job_status = self.request.data.get('status')
        job_id = self.request.data.get('job')
        current_user = self.request.user

        print("ids => ", vertical_id, job_id, current_user)
        print(AppliedJobStatus.objects.filter(vertical_id=vertical_id, job_id=job_id, applied_by=current_user).count())
        if AppliedJobStatus.objects.filter(vertical_id=vertical_id, job_id=job_id, applied_by=current_user).count() != 0:
            return Response({"detail": "Job already assigned to this vertical"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        job_details = JobDetail.objects.get(id=job_id)
        # get current user
        if current_user:
            # make sure the current user apply only one time on one job

            # print(cover_letter, resume, vertical_id)

            obj = AppliedJobStatus.objects.create(job=job_details, applied_by=current_user)
            # if not create:
            #     return Response({'detail': 'User already applied on this job'}, status=status.HTTP_400_BAD_REQUEST, )

            if vertical_id != "":
                obj.vertical_id = vertical_id[0]
            if resume is not None:
                file_name = f"Resume-{vertical_id[0]}"
                resume = upload_pdf(resume[0], file_name)
                obj.resume = resume
            if cover_letter is not None:
                cover_letter = cover_letter[0]
                resp = generate_cover_letter_pdf(cover_letter)
                cover_letter = BytesIO(resp.content)
                file_name = f"CoverLetter-{vertical_id[0]}"
                obj.cover_letter = upload_pdf(cover_letter, file_name)

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
        job_status = self.request.data.get('status', None)
        job = self.request.data.get('job', None)
        obj = AppliedJobStatus.objects.filter(id=job)
        if len(obj) > 0:
            obj = obj.first()
            instance = self.get_queryset().filter(id=self.kwargs.get('job', ''))
            # current use must be the lead
            user_team = Team.objects.filter(reporting_to=request.user, members=obj.applied_by)
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
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            msg = {'detail': 'Applied job id not found'}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)


def generate_cover_letter_pdf(cover_letter):
    template = get_template('cover_letter.html')
    context = {"content": cover_letter}

    # Render the HTML content as a PDF
    html = template.render(context)
    # html = cover_letter
    pdf_file = BytesIO()
    pisa_status = pisa.CreatePDF(BytesIO(html.encode("ISO-8859-1")), pdf_file)
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), pdf_file)
    if not pdf.err:
        return HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    return None
