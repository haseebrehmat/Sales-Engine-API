from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from authentication.serializers.jwt_serializer import JwtSerializer
from authentication.models import User
from authentication.serializers.user_permission import UserPermissionSerializer


class UserPermission(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        queryset = User.objects.filter(pk=pk).first()
        if queryset is not None:
            serializer = UserPermissionSerializer(queryset)
            data = serializer.data
            status_code = status.HTTP_200_OK
        else:
            data = "User not found"
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response(data, status_code)

    def put(self, request, pk):
        group = request.data.get("group")
        if group is not None:
            group = Group.objects.filter(name__iexact=group).first()
            try:
                user = User.objects.get(pk=pk)
                user.groups.add(group)
                message = "Role assigned successfully"
                status_code = status.HTTP_200_OK
            except User.DoesNotExist:
                message = "User doesn't exists"
                status_code = status.HTTP_406_NOT_ACCEPTABLE
        else:
            message = "Group doesn't exists"
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response(message, status_code)

class LoginView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = JwtSerializer
