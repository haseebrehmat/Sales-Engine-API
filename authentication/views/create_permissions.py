from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import CustomPermission, Role
from authentication.utils.permissions import permissions


class CreatePermissions(APIView):

    def get(self, request):
        if request.user.is_superuser:
            self.create_permissions()
            return Response({"detail": "Permissions updated successfully"})
        else:
            return Response({"detail": "Only Admin has access to this endpoint"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def create_permissions(self):
        codenames = CustomPermission.objects.all().values_list("codename", flat=True)
        data = [CustomPermission(**permission) for permission in permissions if permission["codename"] not in codenames]
        data = set(data)
        CustomPermission.objects.bulk_create(data, ignore_conflicts=True)
