from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lead_management.models import Phase, Status, CompanyStatus
from lead_management.serializers import PhaseSerializer
from settings.utils.custom_pagination import CustomPagination
from rest_framework import status


class PhaseList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PhaseSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        name = self.request.GET.get("search", "")
        return Phase.objects.all().filter(name__icontains=name)

    def post(self, request):
        try:
            name = request.data.get('name')
            company_status_id = request.data.get('company_status_id')
            if request.user.profile:
                company_id = request.user.profile.company_id
                company_status = CompanyStatus.objects.filter(pk=company_status_id, company_id=company_id).first()
                if name:
                    name = name.lower()
                    obj = Phase.objects.filter(name=name).first()
                    if not obj:
                        Phase.objects.create(name=name, company_status_id=company_status_id)
                        return Response({'detail': 'Phase Created Successfully!'})
                    else:
                        msg = 'Phase already exist!'
                else:
                    msg = 'Phase name should not be empty!'
                return Response({'detail': msg})
            else:
                return Response({'detail': 'User '})
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)


class PhaseDetail(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            queryset = Phase.objects.get(pk=pk)
            serializer = PhaseSerializer(queryset)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': f'No status exist against id {pk}.'})

    def put(self, request, pk):
        try:
            name = request.data.get('name')
            company_status_id = request.data.get('company_status_id')
            if request.user.profile:
                company_id = request.user.profile.company_id
                company_status = CompanyStatus.objects.filter(pk=company_status_id, company_id=company_id).first()
                if company_status_id != company_status.id:
                    return Response({'detail': 'Company Status doest exist for this company.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                if name:
                    name = name.lower()
                    obj = Phase.objects.get(pk=pk)
                    if obj:
                        obj.name = name
                        obj.company_status_id=company_status_id
                        obj.save()
                        return Response({'detail': 'Phase Updated Successfully!'}, status=status.HTTP_200_OK)
                    else:
                        msg = 'Phase does not not exist!'
                else:
                    msg = 'Phase name should not be empty!'
                return Response({'detail': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response({'detail': 'User '})
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk):
        try:
            obj = Phase.objects.get(pk=pk)
            obj.delete()
            msg = 'Phase deleted successfully!'
        except Exception as e:
            msg = 'Phase doest not exist!'
        return Response({'detail': msg})
