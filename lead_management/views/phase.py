from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from lead_management.models import Phase, Status, CompanyStatus
from lead_management.serializers import PhaseSerializer


class PhaseList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = Phase.objects.all()
        serializer = PhaseSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get('name')
        company_status_id = request.data.get('company_status_id')
        is_active = request.data.get('is_active')
        company_id = request.user.roles.company_id
        company_status = CompanyStatus.objects.filter(pk=company_status_id, company_id=company_id).first()

        if name:
            name = name.lower()
            obj = Phase.objects.filter(name=name).first()
            if not obj:
                Phase.objects.create(name=name, company_status_id=company_status_id, is_active=bool(is_active))
                return Response({'detail': 'Status Created Successfully!'})
            else:
                msg = 'Status already exist!'
        else:
            msg = 'Status name should not be empty!'
        return Response({'detail': msg})


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
        name = request.data.get('name')
        is_active = request.data.get('is_active')
        if name:
            name = name.lower()
            obj = Status.objects.filter(pk=pk).first()
            if obj:
                obj.name = name
                obj.is_active = bool(is_active)
                obj.save()
                return Response({'detail': 'Phase updated Successfully!'})
            else:
                msg = 'No status exist!'
        else:
            msg = 'Phase name is missing!'
        return Response({'detail': msg})

    def delete(self, request, pk):
        try:
            obj = Status.objects.get(pk=pk)
            obj.delete()
            msg = 'Phase deleted successfully!'
        except Exception as e:
            msg = 'Phase doest not exist!'
        return Response({'detail': msg})
