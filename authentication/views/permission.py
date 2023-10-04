import json

from django.apps import apps
from django.db.models import F
from django.db.models.functions import Lower
from django.http import JsonResponse
from numpy.core.defchararray import capitalize
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.exceptions import InvalidUserException
from authentication.models import CustomPermission, Role
from authentication.permissions import RolePermissions
from authentication.serializers.permissions import PermissionSerializer
from rest_framework.generics import ListAPIView
from settings.utils.helpers import serializer_errors


class PermissionView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PermissionSerializer

    def get(self, request):
        modules = set(CustomPermission.objects.annotate(module_name=Lower("module")).values_list('module_name', flat=True))
        data = [{
            'module': capitalize(module),
            'permissions': [
                {
                    'id': x.id,
                    'name': x.name,
                    'codename': x.codename,
                    'level': x.level,
                    'child': x.child,
                    'parent': x.parent,
                } for x in CustomPermission.objects.filter(module__iexact=module)]
        } for module in modules]

        return Response({'data': data, 'modules': modules})

    def post(self, request):
        permissions = json.loads(json.dumps(request.data["permissions"]).lower())
        print(request.data)
        for permission in permissions:
            serializer = PermissionSerializer(data=permission)
            if serializer.is_valid():
                continue
            else:
                data = serializer_errors(serializer)
                if data == "non_field_errors: The fields module, codename, name must make a unique set.":
                    codename = permission["codename"]
                    module = permission["module"]
                    data = f"{codename} permission already exist in {module} module"
                raise InvalidUserException(data)
        serializer.create(request.data)
        message = "Permission created successfully!"
        return Response({'detail': message}, status=status.HTTP_200_OK)


class PermissionDetailView(APIView):
    def get(self, request, pk):
        queryset = CustomPermission.objects.filter(pk=pk).first()
        serializer = PermissionSerializer(queryset, many=False)
        data = serializer.data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = CustomPermission.objects.filter(pk=pk).first()
        serializer = PermissionSerializer(queryset, request.data)
        if not request.data.get("module"):
            return Response({"detail": "Module cannot be empty!"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if serializer.is_valid():
            serializer.save()
            message = "Permission updated successfully!"
            status_code = status.HTTP_200_OK
            return Response({'detail': message}, status=status_code)
        data = serializer_errors(serializer)
        if data == "non_field_errors: The fields module, codename, name must make a unique set.":
            data = "Permission already exist"
        raise InvalidUserException(data)

    def delete(self, request, pk):
        CustomPermission.objects.filter(pk=pk).delete()
        return Response({'detail': "Permission deleted successfully"}, status=status.HTTP_200_OK)


class PermissionAssignmentView(ListAPIView):
    def post(self, request):

        r = request.data.get("role", "")
        if r:
            role = Role.objects.filter(pk=r).first()
            for permission in role.permissions.all():
                role.permissions.remove(permission)
            permissions = request.data.get("permissions", "")
            for permission in permissions:
                custom_permission = CustomPermission.objects.filter(pk=permission).first()
                role.permissions.add(custom_permission)
            message = f"Permissions set for {role.name}"
            status_code = status.HTTP_200_OK
        else:
            message = "Role does not exist!"
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response({'detail': message}, status=status_code)


def get_all_permissions(request):
    models = {
        model.__name__: model for model in apps.get_models()
    }
    exclude_tables = [
        "LogEntry",
        "ContentType",
        "Session",
        "PasswordChangeLogs",
        "ResetPassword",
        "Token",
        "TokenProxy",
        "Permission",
        "Group",
        "CompanyUser",
        "Team",
        "Profile",
        "AppliedJobStatus",
        "BlacklistJobs",
        "View"
    ]
    models = [model for model in list(models) if model not in exclude_tables]

    queryset = CustomPermission.objects.all()
    serializer = PermissionSerializer(queryset, many=True)
    data = serializer.data
    temp = []
    if len(data) > 0:
        for model in models:
            permissions = [{"name": i['name'], "codename": i['codename']} for i in data
                           if model.lower() == i['codename'][len(i['codename']) - len(model)::]]
            temp.append({"module": model, "permission": permissions})
    data = temp

    return JsonResponse(data, status=200, safe=False)
