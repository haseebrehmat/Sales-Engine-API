from io import BytesIO
from settings.utils.helpers import serializer_errors
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db import transaction
from rest_framework.views import APIView
from xhtml2pdf import pisa
from authentication.exceptions import InvalidUserException
from authentication.models import Team
from job_portal.exceptions import NoActiveUserException
from job_portal.models import AppliedJobStatus, JobDetail, RestrictVertical
from job_portal.permissions.applied_job_status import ApplyJobPermission
from job_portal.permissions.change_job import JobStatusPermission
from job_portal.serializers.applied_job import JobStatusSerializer
from job_portal.serializers.restrict_verticals import RestrictVerticalSerializer
from pseudos.models import Verticals
from settings.utils.helpers import is_valid_uuid
from utils.upload_to_s3 import upload_pdf


class ChangeJobStatusView(CreateAPIView, UpdateAPIView):
    serializer_class = JobStatusSerializer
    queryset = AppliedJobStatus.objects.all()
    http_method_names = ['post', 'patch']
    lookup_field = 'id'
    # permission_classes = [ApplyJobPermission | JobStatusPermission, ]
    permission_classes = (AllowAny,)

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        vertical_id = request.data.get("vertical_id", "")
        # getting Team from the vertical
        vertical = Verticals.objects.filter(id=vertical_id).first()
        team = Team.objects.filter(verticals__exact=vertical).first().id

        resume_type = request.data.get('resume_type')
        resume = request.data.get("resume")
        if resume:
            request.data.pop("resume", None)
        else:
            return Response({"detail": "Resume is missing"}, status=status.HTTP_400_BAD_REQUEST)
        cover_letter = request.data.get("cover_letter")
        if cover_letter:
            request.data.pop("cover_letter", None)
        else:
            return Response({"detail": "Cover Letter is missing"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job_status = self.request.data.get('status')
        job_id = self.request.data.get('job')
        current_user = self.request.user

        if AppliedJobStatus.objects.filter(vertical_id=vertical_id, job_id=job_id,
                                           applied_by=current_user).count() != 0:
            return Response({"detail": "Job already assigned to this vertical"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        job_details = JobDetail.objects.get(id=job_id)
        # get current user
        if current_user:
            # make sure the current user apply only one time on one job

            obj = AppliedJobStatus.objects.create(
                job=job_details, applied_by=current_user)
            # if not create:
            #     return Response({'detail': 'User already applied on this job'}, status=status.HTTP_400_BAD_REQUEST, )

            if vertical_id != "":
                obj.vertical_id = vertical_id
                obj.team_id = team
            if resume:
                file_name = f"Resume-{vertical_id}"
                if resume_type == 'manual':
                    obj.is_manual_resume = True
                else:
                    obj.is_manual_resume = False
                resume = upload_pdf(resume, file_name)
                obj.resume = resume
            if cover_letter is not None:
                resp = generate_cover_letter_pdf(cover_letter)
                cover_letter = BytesIO(resp.content)
                file_name = f"CoverLetter-{vertical_id}"
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
                job_result = result.first()
                job_company = job_result.company_name
                vertical_id = request.data.get("vertical_id", "")
                # status = RestrictVertical.objects.create(company_name=job_company, vertical_id = vertical_id)
                data = {"company_name": job_company, "vertical": vertical_id}
                serializer = RestrictVerticalSerializer(data=data, many=False)
                if serializer.is_valid():
                    print("")
                else:
                    data = serializer_errors(serializer)
                    if 'unique set' in data:
                        data = 'This vertical is already hired in this company'
                        raise InvalidUserException(data)
                    else:
                        raise InvalidUserException(data)
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
            user_team = Team.objects.filter(
                reporting_to=request.user, members=obj.applied_by)
            if len(user_team) == 0:
                msg = {'detail': 'User is not a part of the current user team'}
                return Response(msg, status=status.HTTP_200_OK)

            if len(instance) != 0:
                instance.update(job_status=job_status)
                data = JobStatusSerializer(obj, many=False)

                msg = {"data": data.data,
                       'detail': 'Job status updated successfully'}
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
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), pdf_file)
    if not pdf.err:
        return HttpResponse(pdf_file.getvalue(), content_type='application/pdf')

    return None
