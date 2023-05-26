from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from candidate.models import Designation
from candidate.serializers.designation import DesignationSerializer
from settings.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class DesignationListView(ListAPIView):
    serializer_class = DesignationSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Designation.objects.all()
        return queryset

    def post(self, request):
        serializer = DesignationSerializer(data=request.data, many=False)
        if serializer.is_valid():
            data = serializer.validated_data
            serializer.create(data)
            message = "Designation created successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": message}, status_code)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)


class DesignationDetailView(APIView):

    def get(self, request, pk):
        queryset = Designation.objects.filter(pk=pk).first()
        data = []
        if queryset is not None:
            serializer = DesignationSerializer(queryset, many=False)
            data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = Designation.objects.filter(pk=pk).first()
        serializer = DesignationSerializer(instance=queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = "Designaton updated successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": message}, status_code)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)

    def delete(self, request, pk):
        Designation.objects.filter(pk=pk).delete()
        return Response({"detail": "Designaton deleted successfully"}, status.HTTP_200_OK)





