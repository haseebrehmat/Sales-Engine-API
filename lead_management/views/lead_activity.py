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
                obj = Lead.objects.filter(id=lead).first()
                if obj:
                    phase = request.data.get('phase')
                    company_status = request.data.get('status')
                    obj.phase_id = phase
                    obj.company_status_id = company_status
                    obj.save()
                    lead_activity = LeadActivity.objects.create(lead_id=lead.id, company_status_id=company_status,
                                                                phase_id=phase)
                    notes = request.data.get('notes')
                    if notes:
                        LeadActivityNotes.objects.create(lead_activity_id=lead_activity.id, message=notes,
                                                         user_id=request.user.id)
                    return Response({'detail': 'Lead Activity Created Successfully!'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'Invalid lead id'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': serializer_errors(serializer)}, status=status.HTTP_400_BAD_REQUEST)


class LeadActivityDetail(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            queryset = LeadActivity.objects.get(pk=pk)
            serializer = LeadActivitySerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': f'No Lead Activity exist against id {pk}.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            LeadActivity.objects.get(pk=pk).delete()
            msg = 'Lead Activity removed successfully!'
        except Exception as e:
            msg = 'Lead Activity doest not exist!'
        return Response({'detail': msg})
