from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.permissions import UserPermissions
from authentication.serializers.jwt_serializer import JwtSerializer
from authentication.models import User, Profile, Role
from authentication.serializers.user_permission import UserPermissionSerializer
from authentication.serializers.users import UserSerializer
from settings.utils.custom_pagination import CustomPagination
from settings.utils.helpers import validate_password


class UserPermission(APIView):
    permission_classes = (UserPermissions,)

    def get(self, request, pk):
        queryset = User.objects.filter(pk=pk).first()
        if queryset is not None:
            serializer = UserPermissionSerializer(queryset)
            data = serializer.data
            status_code = status.HTTP_200_OK
        else:
            data = {'detail': "User not found"}
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
        return Response({'detail': message}, status_code)


class UserView(ListAPIView):
    permission_classes = (UserPermissions,)
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = self.queryset.filter(profile__company=request.user.profile.company).exclude(id=request.user.id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        status_code = status.HTTP_406_NOT_ACCEPTABLE
        email = request.data.get("email", "")
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        conditions = [
            email != "",
            password != "",
            username != ""
        ]
        if all(conditions):
            if validate_password(password):
                status_code, message = self.create_user(email, password, username, request)

            else:
                message = "Please choose a strong password"

        else:
            message = "Required fields cannot be empty"
        return Response({"detail": message}, status_code)

    def create_user(self, email, password, username, request):
        is_exist = User.objects.filter(email=email)
        if len(is_exist)>0:
            return status.HTTP_400_BAD_REQUEST, "User already exist"
        user = User.objects.create(
            email=email,
            username=username,
            password=make_password(password))


        # Assign permission to all the group

        company_id = request.user.profile.company_id
        if company_id != "":
            Profile.objects.create(user_id=user.id, company_id=company_id)

        role_id = request.data.get("roles", "")
        if role_id != "":
            role = Role.objects.filter(pk=role_id).first()
            if role is not None:
                user.roles = role
        user.save()

        return status.HTTP_200_OK, "User created successfully"


class UserDetailView(APIView):
    permission_classes = (UserPermissions,)

    def get(self, request, pk):
        queryset = User.objects.filter(pk=pk).first()
        serializer = UserSerializer(queryset, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        data = {}
        if username != "":
            data["username"] = username

        if password != "":
            if validate_password(password):
                data["password"] = make_password(password)
            else:
                return Response({"detail": "Please choose a strong password"}, status.HTTP_406_NOT_ACCEPTABLE)
        if email != "":
            data['email'] = email

        user = User.objects.filter(email=email)
        if len(user) == 0:
            user = User.objects.filter(id=pk)
            pass
        else:
            if str(user.first().id) == pk:  # Incase if email is not assign to any user
                pass    # Go update detail
            else:       # Through an error
                return Response({"detail": "User with this email already exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.update(**data)
        user = user.first()
        company_id = request.data.get("company")
        if company_id is not None:
            Profile.objects.filter(user_id=user.id).update(company_id=company_id)

        role_id = request.data.get("roles")
        if role_id is not None:
            role = Role.objects.filter(pk=role_id).first()
            user.roles = role
            user.save()

        return Response({"detail": "User updated successfully"})

    def delete(self, request, pk):
        User.objects.filter(pk=pk).delete()
        return Response({"detail": "User deleted successfully"}, status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = JwtSerializer
