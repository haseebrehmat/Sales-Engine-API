from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from pseudos.models import Verticals
from pseudos.permissions.verticals import VerticalPermissions
from pseudos.serializers.verticals import VerticalSerializer
from pseudos.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class VerticalView(ListAPIView):
    permission_classes = (VerticalPermissions,)
    serializer_class = VerticalSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Verticals.objects.filter(pseudo_id=self.request.GET.get("pseudo_id")).exclude(pseudo_id=None)
        return queryset

    def post(self, request):
        request_data = request.data
        request_data["hobbies"] = request_data.get("hobbies", "")
        if request_data["hobbies"] != "":
            request_data["hobbies"] = ",".join(request_data["hobbies"])

        serializer = VerticalSerializer(data=request_data, many=False)

        if serializer.is_valid():
            serializer.validated_data["verticals_id"] = request.data.get("vertical_id")
            serializer.create(serializer.validated_data)
            message = "Vertical created successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": message}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)


class VerticalDetailView(APIView):
    permission_classes = (VerticalPermissions,)

    def get(self, request, pk):
        queryset = Verticals.objects.filter(pk=pk).first()
        serializer = VerticalSerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = Verticals.objects.filter(pk=pk).first()
        request_data = request.data
        request_data["verticals_id"] = request_data.get("vertical_id")
        request_data["hobbies"] = request_data.get("hobbies", "")
        if request_data["hobbies"] != "":
            request_data["hobbies"] = ",".join(request_data["hobbies"])
        print(request_data["hobbies"])
        serializer = VerticalSerializer(queryset, data=request_data)
        if serializer.is_valid():
            serializer.save(hobbies=request_data["hobbies"])
            message = "Vertical updated successfully"
            status_code = status.HTTP_200_OK
            return Response({"detail": message}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)

    def delete(self, request, pk):
        Verticals.objects.filter(pk=pk).delete()
        return Response({"detail": "Verticals deleted successfully"}, status=status.HTTP_200_OK)
