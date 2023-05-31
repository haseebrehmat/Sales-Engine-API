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
        queryset = Designation.objects.filter(company=self.request.user.profile.company)
        return queryset

    def post(self, request):
        data = request.data
        if not validate_title(request):
            return Response({"detail": "Title already exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = DesignationSerializer(data=data, many=False)
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                data["company_id"] = request.user.profile.company.id
                serializer.create(data)
                message = "Designation created successfully"
                status_code = status.HTTP_201_CREATED
            except Exception as e:
                status_code = status.HTTP_406_NOT_ACCEPTABLE
                if "unique constraint" in str(e):
                    message = "Designation already exist"
                else:
                    message = str(e)
                    print(e)
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
        data = request.data
        if not validate_title(request):
            return Response({"detail": "Title already exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        queryset = Designation.objects.filter(pk=pk).first()
        serializer = DesignationSerializer(instance=queryset, data=data)
        if serializer.is_valid():
            serializer.save(company_id=request.user.profile.company.id)
            message = "Designation updated successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": message}, status_code)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)

    def delete(self, request, pk):
        Designation.objects.filter(pk=pk).delete()
        return Response({"detail": "Designation deleted successfully"}, status.HTTP_200_OK)


def validate_title(request):
    return not Designation.objects.filter(title__iexact=request.data.get("title"),
                                          company=request.user.profile.company).exists()
