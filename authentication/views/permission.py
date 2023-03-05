from django.apps import apps
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.exceptions import InvalidUserException
from authentication.models import CustomPermission
from authentication.permissions import RolePermissions
from authentication.serializers.permissions import PermissionSerializer


from settings.utils.helpers import serializer_errors


class PermissionView(APIView):
    permission_classes = (RolePermissions,)

    def get(self, request):
        queryset = CustomPermission.objects.all()
        if request.GET.get("module", "") != "":
            queryset = queryset.filter(module__iexact=request.GET.get("module"))
        serializer = PermissionSerializer(queryset, many=True)
        data = serializer.data
        if len(data) > 0:
            modules = set([x["module"] for x in data])
            temp = []
            for x in modules:
                temp.append({"module": x, "permissions": [i for i in data if i["module"] == x]})
            data = temp
        else:
            data = []
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            message = "Permission created successfully!"
            status_code = status.HTTP_201_CREATED
            return Response({'detail': message}, status=status_code)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)


class PermissionDetailView(APIView):
    permission_classes = (RolePermissions,)

    def get(self, request, pk):
        queryset = CustomPermission.objects.filter(pk=pk).first()
        serializer = PermissionSerializer(queryset, many=False)
        data = serializer.data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = CustomPermission.objects.filter(pk=pk).first()
        serializer = PermissionSerializer(queryset, request.data)

        if serializer.is_valid():
            serializer.save()

            message = "Permission updated successfully!"
            status_code = status.HTTP_200_OK
            return Response({'detail': message}, status=status_code)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)

    def delete(self, request, pk):
        CustomPermission.objects.filter(pk=pk).delete()
        return Response({'detail': "Permission deleted successfully"}, status=status.HTTP_200_OK)


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
