from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from lead_management.models import Lead, LeadActivity, LeadActivityNotes
from lead_management.serializers import LeadSerializer, LeadActivitySerializer
from settings.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class LeadActivityList(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = LeadSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return LeadActivity.objects.all()

    def post(self, request):
        serializer = LeadActivitySerializer(data=request.data, many=False)

        if serializer.is_valid():
            lead = request.data.get('lead')
            if lead:
                obj = Lead.objects.filter(id=lead)
                if obj.first():
                    company_status = request.data.get('status')
                    phase = request.data.get('phase')
                    candidate = request.data.get('candidate')
                    obj.update(phase_id=phase, company_status_id=company_status, candidate_id=candidate)
                    lead = obj.first()
                    lead_activity = LeadActivity.objects.create(lead=lead, company_status_id=company_status,
                                                                phase_id=phase, candidate_id=candidate)
                    effect_date = request.data.get('effect_date')
                    due_date = request.data.get('due_date')
                    if effect_date:
                        lead_activity.effect_date = effect_date
                    if due_date:
                        lead_activity.due_date = due_date
                    lead_activity.save()
                    notes = request.data.get('notes')
                    if notes:
                        LeadActivityNotes.objects.create(lead_activity_id=lead_activity.id, message=notes,
                                                         user_id=request.user.id)
                    return Response({'detail': 'Lead Activity Created Successfully!'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'Invalid lead id'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'detail': serializer_errors(serializer)}, status=status.HTTP_406_NOT_ACCEPTABLE)


class LeadActivityDetail(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            queryset = LeadActivity.objects.get(pk=pk)
            serializer = LeadActivitySerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': f'No Lead Activity exist against id {pk}.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk):
        try:
            LeadActivity.objects.get(pk=pk).delete()
            msg = 'Lead Activity removed successfully!'
        except Exception as e:
            msg = 'Lead Activity doest not exist!'
        return Response({'detail': msg})
