from io import BytesIO

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

from authentication.models import Team
from job_portal.exceptions import NoActiveUserException
from job_portal.models import AppliedJobStatus, JobDetail
from job_portal.permissions.applied_job_status import ApplyJobPermission
from job_portal.permissions.change_job import JobStatusPermission
from job_portal.serializers.applied_job import JobStatusSerializer
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

        if AppliedJobStatus.objects.filter(vertical_id=vertical_id, job_id=job_id, applied_by=current_user).count() != 0:
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


class Test(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        generate_cover_letter_pdf(data)

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


data = """
<div style="padding: 2rem;">
    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <td style="width: 50%; font-size: 0.875rem;">
                <p style="font-size: 1.25rem; color: #1E40AF;">Usama Jawad</p>
                <p style="color: #4B5563; font-size: 0.625rem; word-break: break-word;">Highly skilled software developer with 7+ years of experience designing and implementing software solutions. Proficient in multiple programming languages such as Java, Python, and JavaScript. Proven ability to develop scalable and high-performance applications using cloud technologies such as AWS and Azure. Demonstrated expertise in full-stack development, including front-end frameworks such as React and back-end frameworks such as Node.js. Strong problem-solving and analytical skills with a passion for delivering clean and efficient code. Excellent communication and collaboration abilities with cross-functional teams and stakeholders</p>
            </td>
            <td style="width: 50%; vertical-align: top;">
                <p style="color: #6B7280; font-size: 0.625rem; text-align: right;">+918888888888</p>
                <p style="color: #1E40AF; fill: currentColor; text-align: right;">
                    <svg width="16" height="16" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <path d="M19 2c0-1.104-.896-2-2-2h-10c-1.104 0-2 .896-2 2v20c0 1.104.896 2 2 2h10c1.104 0 2-.896 2-2v-20zm-8.5 0h3c.276 0 .5.224.5.5s-.224.5-.5.5h-3c-.276 0-.5-.224-.5-.5s.224-.5.5-.5zm1.5 20c-.553 0-1-.448-1-1s.447-1 1-1c.552 0 .999.448.999 1s-.447 1-.999 1zm5-3h-10v-14.024h10v14.024z"></path>
                    </svg>
                </p>
                <p style="color: #6B7280; font-size: 0.625rem; text-align: right;">ubaid@example.com</p>
                <p style="color: #1E40AF; fill: currentColor; text-align: right;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24">
                        <path d="M12 12.713l-11.985-9.713h23.97l-11.985 9.713zm0 2.574l-12-9.725v15.438h24v-15.438l-12 9.725z"></path>
                    </svg>
                </p>
                <p style="color: #6B7280; font-size: 0.625rem; text-align: right;">202 Edyth Green, North Marinaville-21524, South Carolina, USA</p>
                <p style="color: #1E40AF; fill: currentColor; text-align: right;">
                    <svg width="16" height="16" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="true">
                        <path d="M12 1c-3.148 0-6 2.553-6 5.702 0 3.148 2.602 6.907 6 12.298 3.398-5.391 6-9.15 6-12.298 0-3.149-2.851-5.702-6-5.702zm0 8c-1.105 0-2-.895-2-2s.895-2 2-2 2 .895 2 2-.895 2-2 2zm12 14h-24l4-8h3.135c.385.641.798 1.309 1.232 2h-3.131l-2 4h17.527l-2-4h-3.131c.435-.691.848-1.359 1.232-2h3.136l4 8z"></path>
                    </svg>
                </p>
            </td>
        </tr>
    </table>
    
    <div style="margin-bottom: 2.5rem;">
        <p style="font-size: 1.125rem; text-align: center; padding: 0.5rem 0; margin-bottom: 1rem; border-top: 1px solid #000; border-bottom: 1px solid #000; color: #1E40AF; font-weight: 600; text-transform: uppercase;">Skill Set</p>
        <div style="display: flex; flex-direction: column;">
            <!-- Skill set spans go here -->
        </div>
    </div>
    
    <div style="margin-bottom: 2.5rem;">
        <p style="font-size: 1.125rem; text-align: center; padding: 0.5rem 0; margin-bottom: 1rem; border-top: 1px solid #000; border-bottom: 1px solid #000; color: #1E40AF; font-weight: 600; text-transform: uppercase;">Experience</p>
        <div style="display: flex; flex-direction: column;">
            <!-- Experience entries go here -->
        </div>
    </div>
    
    <div style="margin-bottom: 2.5rem;">
        <p style="font-size: 1.125rem; text-align: center; padding: 0.5rem 0; margin-bottom: 1rem; border-top: 1px solid #000; border-bottom: 1px solid #000; color: #1E40AF; font-weight: 600; text-transform: uppercase;">Education History</p>
        <div style="display: flex; flex-direction: column;">
            <!-- Education history entries go here -->
        </div>
    </div>
</div>

"""

resp = generate_cover_letter_pdf(data)
temp = BytesIO(resp.content)
file_name = 'job_portal/output.pdf'

# Read data from BytesIO and write it to a new file
with open(file_name, 'wb') as file:
    file.write(temp.read())
