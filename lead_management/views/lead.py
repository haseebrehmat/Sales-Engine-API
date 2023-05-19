from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from lead_management.models import Lead, LeadActivity, LeadActivityNotes
from lead_management.serializers import LeadSerializer
from lead_management.serializers.lead_serializer import LeadDetailSerializer
from settings.utils.custom_pagination import CustomPagination


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
            lead = Lead.objects.filter(pk=pk)
            company_status = request.data.get('status')
            phase = request.data.get('phase')
            notes = request.data.get('notes')
            if company_status:
                lead.update(company_status_id=company_status, phase_id=phase)
                lead = lead.first()
                lead_activity = LeadActivity.objects.filter(lead=lead, company_status_id=company_status).first()
                if lead_activity:
                    lead_activity.phase_id = phase
                    lead_activity.save()
                else:
                    lead_activity = LeadActivity.objects.create(lead=lead, company_status_id=company_status,
                                                                phase_id=phase)
                effect_date = request.data.get('effect_date')
                due_date = request.data.get('due_date')
                if effect_date:
                    lead_activity.effect_date = effect_date
                if due_date:
                    lead_activity.due_date = due_date
                lead_activity.save()
            if notes:
                LeadActivityNotes.objects.create(lead_activity=lead_activity, message=notes)
            return {"detail": "Lead updated successfully!"}, status.HTTP_200_OK
        except Exception as e:
            return {"detail": str(e)}, status.HTTP_406_NOT_ACCEPTABLE

    def delete(self, request, pk):
        try:
            Lead.objects.get(pk=pk).delete()
            msg = 'Lead removed successfully!'
            status_code = status.HTTP_200_OK
        except Exception as e:
            msg = 'Lead doest not exist!'
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response({'detail': msg}, status=status_code)
