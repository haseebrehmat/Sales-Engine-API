from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from pseudos.models import Verticals
from pseudos.serializers.verticals import VerticalSerializer
from pseudos.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class VerticalView(ListAPIView):
    serializer_class = VerticalSerializer
    pagination_class = CustomPagination
    queryset = Verticals.objects.all()

    def get_queryset(self):
        # self.queryset.filter(company=self.request.user.profile.company)
        return self.queryset

    def post(self, request):
        serializer = VerticalSerializer(data=request.data, many=False)
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

    def get(self, request, pk):
        queryset = Verticals.objects.filter(pk=pk).first()
        serializer = VerticalSerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = Verticals.objects.filter(pk=pk).first()
        request.data["verticals_id"] = request.data.get("vertical_id")
        serializer = VerticalSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = "Vertical updated successfully"
            status_code = status.HTTP_200_OK
            return Response({"detail": message}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)

    def delete(self, request, pk):
        Verticals.objects.filter(pk=pk).delete()
        return Response({"detail": "Verticals deleted successfully"}, status=status.HTTP_200_OK)
