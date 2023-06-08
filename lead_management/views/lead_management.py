import datetime

from django.db import transaction
from rest_framework import status, filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from candidate.utils.custom_pagination import LeadManagementPagination
from job_portal.models import AppliedJobStatus
from lead_management.models import Lead, CompanyStatus, LeadActivity, LeadActivityNotes
from lead_management.serializers import LeadSerializer
from lead_management.serializers.lead_management_serializer import LeadManagementSerializer
from settings.utils.helpers import serializer_errors


class LeadManagement(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = LeadManagementPagination
    serializer_class = LeadManagementSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['company__name', 'status__name']

    def get_queryset(self):
        role = str(self.request.user.roles)
        start_date = self.request.GET.get("start_date", False)
        end_date = self.request.GET.get("end_date", False)
        if "owner" in role.lower():
            queryset = CompanyStatus.objects.filter(company=self.request.user.profile.company).exclude(status=None)
        else:
            queryset = CompanyStatus.objects.filter(company=self.request.user.profile.company).exclude(status=None)
        if start_date and end_date:
            format_string = "%Y-%m-%d"  # Replace with the format of your date string

            # Convert the date string into a datetime object
            start_date = datetime.datetime.strptime(start_date, format_string)
            end_date = datetime.datetime.strptime(end_date, format_string) - datetime.timedelta(seconds=1)
            queryset = queryset.filter(updated_at__range=[start_date, end_date])
        queryset = queryset.order_by("updated_at")


        return queryset


    def post(self, request):
        data, status_code = self.convert_to_lead(request)
        return Response(data, status=status_code)

    @transaction.atomic
    def convert_to_lead(self, request):
        serializer = LeadSerializer(data=request.data, many=False)
        try:
            if serializer.is_valid():
                applied_job_status = request.data.get('job')
                company_status = request.data.get('status')
                phase = request.data.get('phase')
                effect_date = request.data.get('effect_date')
                due_date = request.data.get('due_date')
                notes = request.data.get('notes')
                candidate = request.data.get('candidate')
                lead = Lead.objects.create(applied_job_status_id=applied_job_status, company_status_id=company_status,
                                           phase_id=phase, candidate_id=candidate)
                AppliedJobStatus.objects.filter(id=applied_job_status)\
                    .update(is_converted=True, converted_at=datetime.datetime.now())

                lead_activity = LeadActivity.objects.create(lead_id=lead.id, company_status_id=company_status,
                                                            phase_id=phase, candidate_id=candidate)
                if effect_date:
                    lead_activity.effect_date = effect_date
                if due_date:
                    lead_activity.due_date = due_date
                lead_activity.save()

                if notes:
                    LeadActivityNotes.objects.create(lead_activity=lead_activity, message=notes, user=request.user)
                msg = {'detail': 'Lead Converted successfully!'}
                status_code = status.HTTP_201_CREATED
            else:
                msg = {'detail': serializer_errors(serializer)}
                status_code = status.HTTP_406_NOT_ACCEPTABLE
        except Exception as e:
            msg = {'detail': str(e)}
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return msg, status_code
