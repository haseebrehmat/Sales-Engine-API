from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from pseudos.models import OtherSection
from pseudos.serializers.other_sections import OtherSectionSerializer
from pseudos.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class OtherSectionView(ListAPIView):
    serializer_class = OtherSectionSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        vertical_id = self.request.GET.get("id", "")
        return OtherSection.objects.filter(verticals_d=vertical_id)

    def post(self, request):
        serializer = OtherSectionSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            message = "Other Section created successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": message}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)


class OtherSectionDetailView(APIView):

    def get(self, request, pk):
        queryset = OtherSection.objects.filter(pk=pk).first()
        serializer = OtherSectionSerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = OtherSection.objects.filter(pk=pk).first()
        request_data = request.data
        request_data["verticals_id"] = request.data.get("vertical_id")
        serializer = OtherSectionSerializer(queryset, data=request_data)
        if serializer.is_valid():
            serializer.save()
            message = "Other Section updated successfully"
            status_code = status.HTTP_200_OK
            return Response({"detail": message}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)

    def delete(self, request, pk):
        OtherSection.objects.filter(pk=pk).delete()
        return Response({"detail": "Section deleted successfully"}, status=status.HTTP_200_OK)
