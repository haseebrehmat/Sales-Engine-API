from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from lead_management.models import CompanyStatus
from lead_management.serializers import CompanyStatusSerializer


class CompanyStatusList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = CompanyStatus.objects.all()
        serializer = CompanyStatusSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get('name')
        is_active = request.data.get('is_active')
        if name:
            name = name.lower()
            obj = CompanyStatus.objects.filter(name=name).first()
            if not obj:
                obj = CompanyStatus.objects.create(name=name, is_active=bool(is_active))
                serializer = CompanyStatusSerializer(obj)
                return Response({'detail': 'CompanyStatus Created Successfully!'})
            else:
                msg = 'CompanyStatus already exist!'
        else:
            msg = 'CompanyStatus name should not be empty!'
        return Response({'detail': msg})


class CompanyStatusDetail(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            queryset = CompanyStatus.objects.get(pk=pk)
            serializer = CompanyStatusSerializer(queryset)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': f'No CompanyStatus exist against id {pk}.'})

    def put(self, request, pk):
        name = request.data.get('name')
        is_active = request.data.get('is_active')
        if name:
            name = name.lower()
            obj = CompanyStatus.objects.filter(pk=pk).first()
            if obj:
                obj.name = name
                obj.is_active = bool(is_active)
                obj.save()
                return Response({'detail': 'Company Status Updated Successfully!'})
            else:
                msg = 'No Company Status exist!'
        else:
            msg = 'Company Status name is missing!'
        return Response({'detail': msg})

    def delete(self, request, pk):
        try:
            obj = CompanyStatus.objects.get(pk=pk)
            obj.delete()
            msg = 'Company Status deleted successfully!'
        except Exception as e:
            msg = 'Company Status doest not exist!'
        return Response({'detail': msg})
