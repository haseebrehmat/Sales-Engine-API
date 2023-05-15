from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from lead_management.models import CompanyStatus, Status
from lead_management.serializers import CompanyStatusSerializer


class CompanyStatusList(APIView):
    # permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = CompanyStatus.objects.all()
        serializer = CompanyStatusSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        status_list = request.data.get('status_list')
        if status_list:
            valid_status_ids = list(Status.objects.filter(
                is_active=True).values_list('id', flat=True))
            if [status_id for status_id in status_list if status_id not in valid_status_ids]:
                return Response({"detail": "Incorrect data! Status list consist invalid status ids."})
            company_id = request.user.roles.company_id
            company_status_list = list(CompanyStatus.objects.filter(
                company_id=company_id).values_list('status_id', flat=True))
            CompanyStatus.objects.bulk_create([CompanyStatus(company_id=company_id, status_id=status_id, is_active=True)
                                               for status_id in status_list if status_id not in company_status_list])
            return Response({'detail': 'Company Status Created Successfully!'})
        else:
            return Response({'detail': 'Company Status list is empty!'})


class CompanyStatusDetail(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            queryset = CompanyStatus.objects.get(pk=pk)
            serializer = CompanyStatusSerializer(queryset)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': f'No Company Status exist against id {pk}.'})

    def put(self, request, pk):
        is_active = request.data.get('is_active')
        try:
            CompanyStatus.objects.get(pk=pk).update(is_active=bool(is_active))
            msg = 'Company Status updated successfully!'
        except Exception as e:
            msg = 'Company Status name is missing!'
        return Response({'detail': msg})

    def delete(self, request, pk):
        try:
            CompanyStatus.objects.get(pk=pk).delete()
            msg = 'Company Status deleted successfully!'
        except Exception as e:
            msg = 'Company Status doest not exist!'
        return Response({'detail': msg})
