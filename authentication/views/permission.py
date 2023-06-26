from django.apps import apps
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.exceptions import InvalidUserException
from authentication.models import CustomPermission
from authentication.permissions import RolePermissions
from authentication.serializers.permissions import PermissionSerializer
from rest_framework.generics import ListAPIView


from settings.utils.helpers import serializer_errors


class PermissionView(ListAPIView):
    serializer_class = PermissionSerializer

    def get_queryset(self):
        return CustomPermission.objects.all()


    def post(self, request):
        permissions = request.data["permissions"]
        for permission in permissions:
            serializer = PermissionSerializer(data=permission)
            if serializer.is_valid():
                print("Entered in if")
                continue
            else:
                print("Entered in else")
                data = serializer_errors(serializer)
                if data == "non_field_errors: The fields module, codename, name must make a unique set." :
                    codename = permission["codename"]
                    module = permission["module"]

                    data = f"{codename} permission already exist in {module} module"
                raise InvalidUserException(data)
        serializer.create(request.data)
        message = "Permission created successfully!"
        status_code = status.HTTP_201_CREATED
        return Response({'detail': message}, status=status_code)


class PermissionDetailView(APIView):
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
        if data == "non_field_errors: The fields module, codename, name must make a unique set.":
            data = "Permission already exist"
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
