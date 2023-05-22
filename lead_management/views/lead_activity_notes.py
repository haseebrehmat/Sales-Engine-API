from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from lead_management.models import Lead, LeadActivity, LeadActivityNotes, Phase
from lead_management.serializers import LeadActivityNotesSerializer
from settings.utils.custom_pagination import CustomPagination


class LeadActivityNotesList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        lead = self.request.GET.get('lead')
        lead = Lead.objects.filter(pk=lead).first()
        if lead:
            company_status = self.request.GET.get('status')
            phase = self.request.GET.get('phase')
            queryset = LeadActivity.objects.filter(lead_id=lead)
            if not company_status and not phase:
                queryset = queryset.filter(company_status=lead.company_status, phase=lead.phase)
            else:
                queryset = queryset.filter(company_status_id=company_status)
                if phase:
                    queryset = queryset.filter(phase_id=phase)
                else:
                    queryset = queryset.filter(phase=None)
            lead_activities_ids = list(queryset.values_list('id', flat=True))
            notes_queryset = LeadActivityNotes.objects.filter(lead_activity_id__in=lead_activities_ids)
        else:
            notes_queryset = LeadActivityNotes.objects.none()
        serializer = LeadActivityNotesSerializer(notes_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        lead = request.data.get('lead')
        lead = Lead.objects.filter(pk=lead).first()
        if lead:
            lead_activity = LeadActivity.objects.filter(lead=lead, company_status=lead.company_status,
                                                        phase=lead.phase).first()
            notes = request.data.get('notes')
            if notes:
                lead_activity_notes = LeadActivityNotes.objects.create(lead_activity=lead_activity, message=notes,
                                                                       user=request.user)
                return Response({'detail': 'Lead Activity Notes Created Successfully!'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'Notes should not be empty.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'detail': 'Lead id is not correct.'}, status=status.HTTP_406_NOT_ACCEPTABLE)


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

    def put(self, request, pk):
        try:
            notes = LeadActivityNotes.objects.get(pk=pk)
            if notes.user_id == request.user.id:
                notes.message = request.data.get('notes')
                notes.save()
                msg = 'Lead Activity Notes Updated Successfully!'
                status_code = status.HTTP_200_OK
            else:
                msg = 'You are not allowed to edit this notes!'
                status_code = status.HTTP_406_NOT_ACCEPTABLE
            return Response({'detail': msg}, status=status_code)
        except Exception as e:
            return Response({'detail': f'No Lead Activity Notes exist against id {pk}.'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk):
        try:
            notes = LeadActivityNotes.objects.get(pk=pk)
            if notes.user_id == request.user.id:
                notes.delete()
                msg = 'Lead Activity Notes removed successfully!'
                status_code = status.HTTP_200_OK
            else:
                msg = 'You are not allowed to delete this notes.'
                status_code = status.HTTP_406_NOT_ACCEPTABLE
        except Exception as e:
            msg = 'Lead Activity Notes doest not exist!'
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response({'detail': msg}, status=status_code)
