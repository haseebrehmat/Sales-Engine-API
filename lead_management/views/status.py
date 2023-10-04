from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from lead_management.models import Status, CompanyStatus, Lead
from lead_management.serializers import StatusSerializer
from rest_framework.response import Response
from settings.utils.custom_pagination import CustomPagination
from rest_framework.generics import ListAPIView
from rest_framework import status
from settings.utils.helpers import serializer_errors


class StatusList(ListAPIView):
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = StatusSerializer

    def get_queryset(self):
        name = self.request.GET.get('search', "")
        queryset = Status.objects.all().filter(name__icontains=name)
        print(queryset.count())
        return queryset

    def post(self, request):
        serializer = StatusSerializer(data=request.data, many=False)
        if serializer.is_valid():
            name = request.data.get('name')
            if name:
                name = name.lower()
                obj = Status.objects.filter(name=name).first()
                if not obj:
                    Status.objects.create(name=name, is_active=True)
                    return Response({'detail': 'Status Created Successfully!'}, status=status.HTTP_201_CREATED)
                else:
                    msg = 'Status already exist!'
            else:
                msg = 'Status name should not be empty!'
            return Response({'detail': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'detail': serializer_errors(serializer)}, status=status.HTTP_406_NOT_ACCEPTABLE)


class AllStatuses(APIView):
    def get(self, request):
        if request.user.profile:
            company_id = request.user.profile.company_id
            company_statuses_ids = list(
                CompanyStatus.objects.filter(company_id=company_id).values_list('status_id', flat=True))
            queryset = Status.objects.exclude(id__in=company_statuses_ids)
            serializer = StatusSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User must have company id."}, status=status.HTTP_406_NOT_ACCEPTABLE)


class StatusDetail(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            queryset = Status.objects.get(pk=pk)
            serializer = StatusSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': f'No status exist against id {pk}.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def put(self, request, pk):
        name = request.data.get('name')
        is_active = request.data.get('is_active')
        if name:
            name = name.lower()
            obj = Status.objects.filter(pk=pk).first()
            if obj:
                obj.name = name
                obj.is_active = bool(is_active)
                obj.save()
                return Response({'detail': 'Status Updated Successfully!'}, status=status.HTTP_200_OK)
            else:
                msg = 'No status exist!'
        else:
            msg = 'Status name is missing!'
        return Response({'detail': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk):
        try:
            obj = Status.objects.get(pk=pk)
            leads = Lead.objects.filter(company_status__status=obj)
            lead_activities = Lead.objects.filter(company_status__status=obj)
            if leads or lead_activities:
                msg = 'This status cannot be deleted because it is used by lead.'
                status_code = status.HTTP_406_NOT_ACCEPTABLE
            else:
                obj.delete()
                msg = 'Status deleted successfully!'
                status_code = status.HTTP_200_OK
        except Exception as e:
            msg = 'Status doest not exist!'
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response({'detail': msg}, status=status_code)
