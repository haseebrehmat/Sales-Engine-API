from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from lead_management.models import CompanyStatus, Status
from lead_management.serializers import CompanyStatusSerializer, CompanyStatusPhasesSerializer
from settings.utils.custom_pagination import CustomPagination
from rest_framework import status


class CompanyStatusList(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = CompanyStatusSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return CompanyStatus.objects.all().exclude(status__isnull=True)

    def post(self, request):
        serializer = CompanyStatusPhasesSerializer(data=request.data, many=False)
        if not serializer.is_valid():
            return Response({'detail': serializer.errors[0]}, status=status.HTTP_400_BAD_REQUEST)
        status_list = request.data.get('status_list')
        if status_list:
            company_id = request.user.profile.company_id
            company_statuses_ids = list(CompanyStatus.objects.filter(company_id=company_id).values_list('status_id', flat=True))
            valid_status_ids = list(Status.objects.exclude(id__in=company_statuses_ids).values_list('id', flat=True))
            for status_id in status_list:
                if status_id not in valid_status_ids:
                    return Response({"detail": "Incorrect data! Status list consist invalid status ids."},
                                    status=status.HTTP_400_BAD_REQUEST)
            company_status_list = list(CompanyStatus.objects.filter(
                company_id=company_id).values_list('status_id', flat=True))
            CompanyStatus.objects.bulk_create([CompanyStatus(company_id=company_id, status_id=status_id, is_active=True)
                                               for status_id in status_list if status_id not in company_status_list])
            return Response({'detail': 'Company Status Created Successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Company Status list is empty!'}, status=status.HTTP_400_BAD_REQUEST)


class AllCompanyStatuses(APIView):
    def get(self, request):
        if request.user.profile:
            company_id = request.user.profile.company_id
            queryset = CompanyStatus.objects.filter(company_id=company_id, is_active=True)
            serializer = CompanyStatusSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User must have company id."}, status=status.HTTP_400_BAD_REQUEST)


class CompanyStatusPhases(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            if request.user.profile.company_id:
                queryset = CompanyStatus.objects.exclude(status=None).filter(company_id=request.user.profile.company_id)
                serializer = CompanyStatusPhasesSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': "User must have company id."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class CompanyStatusDetail(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            queryset = CompanyStatus.objects.get(pk=pk)
            serializer = CompanyStatusSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': f'No Company Status exist against id {pk}.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            CompanyStatus.objects.get(pk=pk).delete()
            msg = 'Company Status removed successfully!'
        except Exception as e:
            msg = 'Company Status doest not exist!'
        return Response({'detail': msg})
