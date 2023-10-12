from rest_framework import status, filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.exceptions import InvalidUserException
from authentication.models.company import Company
from authentication.permissions import CompanyPermissions
from authentication.serializers.company import CompanySerializer
from settings.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class CompanyView(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = CompanySerializer

    permission_classes = (CompanyPermissions,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code']

    def get_queryset(self):
        return Company.objects.all()

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            data = "Company created successfully"
            status_code = status.HTTP_201_CREATED

            return Response({"detail": data}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)


class CompanyDetailView(APIView):
    permission_classes = (CompanyPermissions,)

    def get(self, request, pk):
        company = Company.objects.filter(pk=pk).first()
        serializer = CompanySerializer(company, many=False)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = Company.objects.filter(pk=pk).first()
        data = request.data
        serializer = CompanySerializer(queryset, data)

        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_200_OK
            message = {"detail": "Company updated successfully"}
            return Response(message, status=status_code)

        data = serializer_errors(serializer)
        raise InvalidUserException(data)
