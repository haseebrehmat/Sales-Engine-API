from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from lead_management.models import CompanyStatus, Status, Lead
from lead_management.serializers import CompanyStatusSerializer, CompanyStatusPhasesSerializer
from settings.utils.custom_pagination import CustomPagination


class CompanyStatusList(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = CompanyStatusSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        search = self.request.GET.get("search", "")
        return CompanyStatus.objects.filter(status__name__icontains=search, company=self.request.user.profile.company).exclude(status__isnull=True)

    def post(self, request):
        serializer = CompanyStatusPhasesSerializer(data=request.data, many=False)
        if not serializer.is_valid():
            return Response({'detail': serializer.errors[0]}, status=status.HTTP_406_NOT_ACCEPTABLE)
        status_list = request.data.get('status_list')
        if status_list:
            company_id = request.user.profile.company_id
            company_statuses_ids = list(CompanyStatus.objects.filter(company_id=company_id).values_list('status_id', flat=True))
            valid_status_ids = list(Status.objects.exclude(id__in=company_statuses_ids).values_list('id', flat=True))
            for status_id in status_list:
                if status_id not in valid_status_ids:
                    return Response({"detail": "Incorrect data! Status list consist invalid status ids."},
                                    status=status.HTTP_406_NOT_ACCEPTABLE)
            company_status_list = list(CompanyStatus.objects.filter(
                company_id=company_id).values_list('status_id', flat=True))
            CompanyStatus.objects.bulk_create([CompanyStatus(company_id=company_id, status_id=status_id, is_active=True)
                                               for status_id in status_list if status_id not in company_status_list])
            return Response({'detail': 'Company Status Created Successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Company Status list is empty!'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class AllCompanyStatuses(APIView):
    def get(self, request):
        if request.user.profile:
            company_id = request.user.profile.company_id
            queryset = CompanyStatus.objects.filter(company_id=company_id, is_active=True)
            serializer = CompanyStatusSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User must have company id."}, status=status.HTTP_406_NOT_ACCEPTABLE)


class CompanyStatusPhases(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            if request.user.profile.company_id:
                queryset = CompanyStatus.objects.exclude(status=None).filter(company_id=request.user.profile.company_id)
                serializer = CompanyStatusPhasesSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': "User must have company id."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)


class CompanyStatusDetail(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            queryset = CompanyStatus.objects.get(pk=pk)
            serializer = CompanyStatusSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': f'No Company Status exist against id {pk}.'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk):
        try:
            obj = CompanyStatus.objects.get(pk=pk)
            leads = Lead.objects.filter(company_status=obj)
            lead_activities = Lead.objects.filter(company_status=obj)
            if leads or lead_activities:
                msg = 'This company status cannot be deleted because it is used in some leads.'
                status_code = status.HTTP_406_NOT_ACCEPTABLE
            else:
                obj.delete()
                msg = 'Company Status removed successfully!'
                status_code = status.HTTP_200_OK
        except Exception as e:
            msg = 'Company Status doest not exist!'
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response({'detail': msg}, status=status_code)
