from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from job_portal.models import RestrictVertical
from job_portal.utils.detect_changes import detect_model_changes
from lead_management.models import Lead, LeadActivity, LeadActivityNotes
from lead_management.serializers import LeadSerializer
from lead_management.serializers.lead_serializer import LeadDetailSerializer
from job_portal.serializers.restrict_verticals import RestrictVerticalSerializer
from settings.utils.custom_pagination import CustomPagination
from lead_management.models.company_status import CompanyStatus

class LeadList(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = LeadSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Lead.objects.all()


class LeadDetail(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            queryset = Lead.objects.get(pk=pk)
            serializer = LeadDetailSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': f'No Lead exist against id {pk}.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def put(self, request, pk):
        data, status_code = self.update_lead(request, pk)
        return Response(data, status=status_code)

    @transaction.atomic
    def update_lead(self, request, pk):
        try:
            flag = True
            new_data = {}
            old_data = {}

            lead = Lead.objects.filter(pk=pk)
            old_data['id'] = lead.first()
            company_status = request.data.get('status')
            phase = request.data.get('phase')
            notes = request.data.get('notes')
            candidate = request.data.get('candidate')

            if not company_status and not phase and candidate:
                # update candidate on lead
                old_data['candidate_id'] = lead.first().candidate_id
                lead.update(candidate_id=candidate)
                lead.update(edited=True)
                new_data['candidate_id'] = candidate
                lead = lead.first()
                lead_activity = LeadActivity.objects.filter(lead=lead, company_status=lead.company_status,
                                                            phase=lead.phase, candidate_id=candidate).first()

                if not lead_activity:
                    flag = False
                    lead_activity = LeadActivity.objects.create(lead=lead, company_status=lead.company_status,
                                                                phase=lead.phase, candidate_id=candidate)
            elif company_status:
                # update company_status and phase_id
                old_data['company_status_id'] = lead.first().company_status_id
                old_data['phase_id'] = lead.first().phase_id
                lead.update(company_status_id=company_status, phase_id=phase)
                # here is a logic of create object in restrict_vertical
                if CompanyStatus.objects.filter(pk=company_status).first().status.name == 'hired':
                    job_company, vertical_id = self.get_company_vertical(lead.first().id)
                    data = {"company_name": job_company, "vertical": vertical_id}
                    serializer = RestrictVerticalSerializer(data=data, many=False)
                    if serializer.is_valid():
                        data = serializer.validated_data
                        serializer.create(data)
                    else:
                        print("Error")

                lead.update(edited=True)
                new_data['company_status_id'] = company_status
                new_data['phase_id'] = phase
                lead = lead.first()
                lead_activity = LeadActivity.objects.filter(lead=lead, company_status_id=company_status, phase_id=phase,
                                                            candidate=lead.candidate).first()
                if lead_activity:
                    lead_activity.phase_id = phase
                    lead_activity.save()
                else:
                    lead_activity = LeadActivity.objects.create(lead=lead, company_status_id=company_status,
                                                                phase_id=phase, candidate=lead.candidate)
                effect_date = request.data.get('effect_date')
                due_date = request.data.get('due_date')
                if effect_date:
                    old_data['effect_date'] = lead_activity.effect_date
                    lead_activity.effect_date = effect_date
                    if flag:
                        new_data['effect_date'] = effect_date
                if due_date:
                    old_data['due_date'] = lead_activity.due_date
                    lead_activity.due_date = due_date
                    if flag:
                        new_data['due_date'] = due_date
                lead_activity.save()
            if notes:
                LeadActivityNotes.objects.create(lead_activity=lead_activity, message=notes)

            detect_model_changes(old_data, new_data, Lead, request.user)
            return {"detail": "Lead updated successfully!"}, status.HTTP_200_OK
        except Exception as e:
            return {"detail": str(e)}, status.HTTP_406_NOT_ACCEPTABLE

    def delete(self, request, pk):
        try:
            lead = Lead.objects.get(pk=pk)
            job_company, vertical_id = self.get_company_vertical(lead.id)
            RestrictVertical.objects.filter(company_name=job_company, vertical=vertical_id).first().delete()
            lead.delete()
            msg = 'Lead removed successfully!'
            status_code = status.HTTP_200_OK
        except Exception as e:
            msg = 'Lead doest not exist!'
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response({'detail': msg}, status=status_code)

    def get_company_vertical(self, lead_id):
        lead = Lead.objects.filter(pk=lead_id).first()
        company_name = lead.applied_job_status.job.company_name
        vertical = lead.applied_job_status.vertical_id
        return company_name, vertical
