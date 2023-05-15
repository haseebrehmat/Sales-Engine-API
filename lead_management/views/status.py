from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from lead_management.models import Status
from lead_management.serializers import StatusSerializer
from rest_framework.response import Response

class StatusList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = Status.objects.all()
        serializer = StatusSerializer(queryset, many=True)
        return Response(serializer.data)


    def post(self, request):
        name = request.data.get('name')
        is_active = request.data.get('is_active')
        if name:
            name = name.lower()
            obj = Status.objects.filter(name=name).first()
            if not obj:
                obj = Status.objects.create(name=name, is_active=bool(is_active))
                serializer = StatusSerializer(obj)
                return Response({'detail': 'Status Created Successfully!'})
            else:
                msg = 'Status already exist!'
        else:
            msg = 'Status name should not be empty!'
        return Response({'detail': msg})


class StatusDetail(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            queryset = Status.objects.get(pk=pk)
            serializer = StatusSerializer(queryset)
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
                return Response({'detail': 'Status Updated Successfully!'})
            else:
                msg = 'No status exist!'
        else:
            msg = 'Status name is missing!'
        return Response({'detail': msg})


    def delete(self, request, pk):
        try:
            obj = Status.objects.get(pk=pk)
            obj.delete()
            msg = 'Status deleted successfully!'
        except Exception as e:
            msg = 'Status doest not exist!'
        return Response({'detail': msg})
