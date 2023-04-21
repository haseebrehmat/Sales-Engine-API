from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from pseudos.models import CoverLetter
from pseudos.permissions.verticals import VerticalPermissions
from pseudos.serializers.cover_letter import CoverLetterSerializer
from pseudos.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class CoverLetterView(ListAPIView):
    permission_classes = (VerticalPermissions,)
    serializer_class = CoverLetterSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        vertical_id = self.request.GET.get("id")
        return CoverLetter.objects.filter(vertical_id=vertical_id).exclude(vertical_id=None)

    def post(self, request):
        vertical_id = request.data.get("vertical_id")
        if vertical_id is not None:
            if CoverLetter.objects.filter(vertical_id=vertical_id).count() == 0:
                CoverLetter.objects.create(vertical_id=vertical_id, template=request.data.get("template", ""))
            else:
                CoverLetter.objects.filter(vertical_id=vertical_id).update(template=request.data.get("template", ""))
            message = {"detail": "Cover letter saved successfully"}
            status_code = status.HTTP_200_OK
        else:
            message = {"detail": "Vertical ID cannot be empty"}
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response(message, status_code)


class CoverLetterDetailView(APIView):
    permission_classes = (VerticalPermissions,)

    def get(self, request, pk):
        queryset = CoverLetter.objects.filter(pk=pk).first()
        serializer = CoverLetterSerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = CoverLetter.objects.filter(pk=pk).first()
        request_data = request.data
        serializer = CoverLetterSerializer(queryset, data=request_data)
        if serializer.is_valid():
            serializer.save(vertical_id=request.data.get("vertical_id"))
            message = "Cover letter updated successfully"
            status_code = status.HTTP_200_OK
            return Response({"detail": message}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)

    def delete(self, request, pk):
        CoverLetter.objects.filter(pk=pk).delete()
        return Response({"detail": "Cover letter deleted successfully"}, status=status.HTTP_200_OK)
