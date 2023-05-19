from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from lead_management.models import LeadActivity, LeadActivityNotes
from lead_management.serializers import LeadActivityNotesSerializer
from settings.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class LeadActivityNotesList(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = LeadActivityNotesSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        lead = self.request.GET.get('lead')
        company_status = self.request.GET.get('status')
        phase = self.request.GET.get('phase')
        lead_activities_ids = list(LeadActivity.objects.filter(lead_id=lead).values_list('id', flat=True))
        return LeadActivityNotes.objects.filter(lead_activity_id__in=lead_activities_ids)

    def post(self, request):
        serializer = LeadActivityNotesSerializer(data=request.data, many=False)

        if serializer.is_valid():
            lead_activity_id = request.data.get('lead_activity')
            lead_activity = LeadActivity.objects.filter(pk=lead_activity_id).first()
            notes = request.data.get('notes')
            if notes:
                lead_activity_notes = LeadActivityNotes.objects.create(lead_activity=lead_activity, message=notes,
                                                                       user=request.user)
                return Response({'detail': 'Lead Activity Notes Created Successfully!'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'Notes should not be empty.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'detail': serializer_errors(serializer)}, status=status.HTTP_406_NOT_ACCEPTABLE)


class LeadActivityNotesDetail(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            queryset = LeadActivityNotes.objects.get(pk=pk)
            serializer = LeadActivityNotesSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': f'No Lead Activity Notes exist against id {pk}.'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk):
        try:
            LeadActivityNotes.objects.get(pk=pk).delete()
            msg = 'Lead Activity Notes removed successfully!'
        except Exception as e:
            msg = 'Lead Activity Notes doest not exist!'
        return Response({'detail': msg})
