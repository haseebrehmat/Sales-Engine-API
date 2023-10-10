from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission, Group
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.serializers.group import GroupSerializer
from settings.utils.permission_managers import UserPermissions


def get_permission(app, group):
    group = Group.objects.filter(name__iexact=group).first()
    permissions = Permission.objects.filter(group=group, content_type__app_label=app)
    permissions = [permission.codename for permission in permissions]
    return permissions


class GroupView(APIView):
    permission_classes = (UserPermissions,)
    # permission_required = get_permission("authentication", "Tenant Access")
    # permission_denied_message = "You don't have access to this endpoint"

    def get(self, request):
        queryset = Group.objects.all()
        serializer = GroupSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GroupSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            data["permissions"] = request.data.get("permissions")
            serializer.create(data)

            message = "Group created successfully!"
            status_code = status.HTTP_201_CREATED
        else:
            message = serializer.errors
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response(message, status=status_code)


class GroupDetailView(APIView):
    permission_classes = (UserPermissions,)

    def get(self, request, pk):
        queryset = Group.objects.filter(pk=pk).first()
        serializer = GroupSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = Group.objects.filter(pk=pk).first()
        serializer = GroupSerializer(queryset, request.data)

        if serializer.is_valid():
            serializer.save(permissions=request.data.get("permissions"))

            message = "Group updated successfully!"
            status_code = status.HTTP_200_OK
        else:
            message = serializer.errors
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response(message, status=status_code)

    def delete(self, request, pk):
        Group.objects.filter(pk=pk).delete()
        return Response("Group deleted successfully", status=status.HTTP_200_OK)



