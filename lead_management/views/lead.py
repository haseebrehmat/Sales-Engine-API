from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from lead_management.models import CompanyStatus, Status, Lead
from lead_management.serializers import LeadSerializer
from settings.utils.custom_pagination import CustomPagination
from rest_framework import status


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
        else:
            return Response({'detail': serializer.errors[0]}, status=status.HTTP_400_BAD_REQUEST)


class CompanyStatusDetail(APIView):
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
