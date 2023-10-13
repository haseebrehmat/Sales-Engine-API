from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from authentication.models.company import CompanyAPIIntegration
from authentication.permissions import IntegrationPermissions
from authentication.serializers.company import CompanyAPIIntegrationSerializer
from settings.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors
from django.db.models import Q


class IntegrationView(ListAPIView):
    permission_classes = (IntegrationPermissions, )
    pagination_class = CustomPagination
    serializer_class = CompanyAPIIntegrationSerializer

    def get_queryset(self):
        search = self.request.GET.get("search", "")
        if self.request.user.is_superuser:
            queryset = CompanyAPIIntegration.objects.all()
            if search != "":
                name_query = Q(name__icontains=search)
                company_query = Q(company__name__icontains=search)
                queryset = queryset.filter(name_query | company_query)
        else:
            queryset = CompanyAPIIntegration.objects.filter(company__profile__user=self.request.user)
            if search != "":
                queryset = queryset.filter(name__icontains=search)
        return queryset

    def post(self, request):
        serializer = CompanyAPIIntegrationSerializer(data=request.data, many=False)
        if serializer.is_valid():
            data = serializer.validated_data
            data["company_id"] = request.data.get("company")
            serializer.create(serializer.validated_data)
            return Response({"detail": "Integration created successfully"}, status.HTTP_201_CREATED)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)


class IntegrationDetailView(APIView):
    permission_classes = (IntegrationPermissions, )

    def get(self, request, pk):
        queryset = CompanyAPIIntegration.objects.filter(pk=pk).first()
        serializer = CompanyAPIIntegrationSerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = CompanyAPIIntegration.objects.filter(pk=pk).first()
        serializer = CompanyAPIIntegrationSerializer(queryset, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Integration updated successfully"}, status=status.HTTP_200_OK)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)

    def delete(self, request, pk):
        CompanyAPIIntegration.objects.filter(pk=pk).delete()
        return Response({"detail": "Integration deleted successfully"}, status.HTTP_200_OK)
