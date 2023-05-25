import datetime

from django.db import transaction
from rest_framework import status, filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from job_portal.models import AppliedJobStatus
from lead_management.models import Lead, CompanyStatus, LeadActivity, LeadActivityNotes
from lead_management.serializers import LeadSerializer
from lead_management.serializers.lead_management_serializer import LeadManagementSerializer
from settings.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class LeadManagement(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    serializer_class = LeadManagementSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['company__name', 'status__name']

    def get_queryset(self):
        role = str(self.request.user.roles)
        if "owner" in role.lower():
            queryset = CompanyStatus.objects.filter(company=self.request.user.profile.company).exclude(status=None)
        else:
            queryset = CompanyStatus.objects.filter(company=self.request.user.profile.company).exclude(status=None)

        return queryset

    def post(self, request):
        data, status_code = self.convert_to_lead(request)
        return Response(data, status=status_code)

    @transaction.atomic
    def convert_to_lead(self, request):
        serializer = LeadSerializer(data=request.data, many=False)

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
            return {'detail': 'Lead Converted successfully!'}, status.HTTP_201_CREATED
        else:
            return {'detail': serializer_errors(serializer)}, status.HTTP_406_NOT_ACCEPTABLE
