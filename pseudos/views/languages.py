from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from pseudos.models import Language
from pseudos.permissions.verticals import VerticalPermissions
from pseudos.serializers.languages import LanguageSerializer
from pseudos.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class LanguageView(ListAPIView):
    permission_classes = (VerticalPermissions,)
    serializer_class = LanguageSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        vertical_id = self.request.GET.get("id")
        return Language.objects.filter(vertical_id=vertical_id).exclude(vertical_id=None)

    def post(self, request):
        serializer = LanguageSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.validated_data["vertical_id"] = request.data.get("vertical_id")
            serializer.create(serializer.validated_data)
            message = "Language created successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": message}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)


class LanguageDetailView(APIView):
    permission_classes = (VerticalPermissions,)

    def get(self, request, pk):
        queryset = Language.objects.filter(pk=pk).first()
        serializer = LanguageSerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = Language.objects.filter(pk=pk).first()
        request_data = request.data
        request_data["vertical_id"] = request.data.get("vertical_id")
        serializer = LanguageSerializer(queryset, data=request_data)
        if serializer.is_valid():
            serializer.save()
            message = "Language updated successfully"
            status_code = status.HTTP_200_OK
            return Response({"detail": message}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)

    def delete(self, request, pk):
        Language.objects.filter(pk=pk).delete()
        return Response({"detail": "Language deleted successfully"}, status=status.HTTP_200_OK)
