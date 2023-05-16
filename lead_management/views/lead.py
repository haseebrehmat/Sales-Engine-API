from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from lead_management.models import Lead, LeadActivity, LeadActivityNotes
from lead_management.serializers import LeadSerializer
from settings.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors

class LeadList(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = LeadSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Lead.objects.all()

    def post(self, request):
        serializer = LeadSerializer(data=request.data, many=False)

        if serializer.is_valid():
            applied_job_status = request.data.get('applied_job_status')
            company_status = request.data.get('company_status')
            phase = request.data.get('phase')
            effect_date = request.data.get('effect_date')
            due_date = request.data.get('due_date')
            notes = request.data.get('notes')
            lead = Lead.objects.create(applied_job_status_id=applied_job_status, company_status_id=company_status,
                                       phase_id=phase)
            lead_activity = LeadActivity.objects.create(lead_id=lead.id, company_status_id=company_status,
                                                        phase_id=phase)
            if effect_date:
                lead_activity.effect_date = effect_date
            if due_date:
                lead_activity.due_date = due_date
            lead_activity.save()
            if notes:
                LeadActivityNotes.objects.create(lead_activity_id=lead_activity.id, message=notes, user=request.user.id)
            return Response({'detail': 'Lead created successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': serializer_errors(serializer)}, status=status.HTTP_400_BAD_REQUEST)


class LeadDetail(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            queryset = Lead.objects.get(pk=pk)
            serializer = LeadSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': f'No Lead exist against id {pk}.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            Lead.objects.get(pk=pk).delete()
            msg = 'Lead removed successfully!'
        except Exception as e:
            msg = 'Lead doest not exist!'
        return Response({'detail': msg})
