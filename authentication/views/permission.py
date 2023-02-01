from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.serializers.permissions import PermissionSerializer


class PermissionView(APIView):

    def get(self, request):
        queryset = Permission.objects.all()
        serializer = PermissionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PermissionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.create(serializer.validated_data)

            message = "Permission created successfully!"
            status_code = status.HTTP_201_CREATED
        else:
            message = serializer.errors
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response(message, status=status_code)


class PermissionDetailView(APIView):

    def get(self, request, pk):
        queryset = Permission.objects.filter(pk=pk).first()
        serializer = PermissionSerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = Permission.objects.filter(pk=pk).first()
        serializer = PermissionSerializer(queryset, request.data)

        if serializer.is_valid():
            serializer.save()

            message = "Permission updated successfully!"
            status_code = status.HTTP_200_OK
        else:
            message = serializer.errors
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response(message, status=status_code)

    def delete(self, request, pk):
        Permission.objects.filter(pk=pk).delete()
        return Response("Permission deleted successfully", status=status.HTTP_200_OK)

