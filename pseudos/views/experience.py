from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from pseudos.models import Experience
from pseudos.permissions.verticals import VerticalPermissions
from pseudos.serializers.experience import ExperienceSerializer
from pseudos.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class ExperienceView(ListAPIView):
    permission_classes = (VerticalPermissions,)
    serializer_class = ExperienceSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        vertical_id = self.request.GET.get("id")
        return Experience.objects.filter(vertical_id=vertical_id).exclude(vertical_id=None)

    def post(self, request):
        serializer = ExperienceSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.validated_data["vertical_id"] = request.data.get("vertical_id")
            serializer.create(serializer.validated_data)
            message = "Experience created successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": message}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)


class ExperienceDetailView(APIView):
    permission_classes = (VerticalPermissions,)

    def get(self, request, pk):
        queryset = Experience.objects.filter(pk=pk).first()
        serializer = ExperienceSerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = Experience.objects.filter(pk=pk).first()
        request_data = request.data
        request_data["vertical_id"] = request.data.get("vertical_id")
        serializer = ExperienceSerializer(queryset, data=request_data)
        if serializer.is_valid():
            serializer.save()
            message = "Experience updated successfully"
            status_code = status.HTTP_200_OK
            return Response({"detail": message}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)

    def delete(self, request, pk):
        Experience.objects.filter(pk=pk).delete()
        return Response({"detail": "Experience deleted successfully"}, status=status.HTTP_200_OK)
