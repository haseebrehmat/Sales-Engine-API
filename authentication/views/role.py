from rest_framework import status, filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import Role, User, MultipleRoles
from authentication.permissions import RolePermissions
from authentication.serializers.role import RoleSerializer
from authentication.serializers.users import UserSerializer
from settings.utils.custom_pagination import CustomPagination


class RoleView(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    permission_classes = (RolePermissions,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'company__name', 'permissions__name', 'permissions__module']

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        print(self.request.user.profile)
        if self.request.user.is_superuser:
            queryset = queryset.filter(company_id=None).exclude(id=self.request.user.roles.id)
        else:
            queryset = queryset.filter(company__profile__user=self.request.user)
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        fix_roles = [
            "admin",
            "owner"
        ]
        if request.data.get("name").lower() in fix_roles:
            return Response({"detail": f"You cannot create role with name '{request.data.get('name')}'"},
                            status.HTTP_406_NOT_ACCEPTABLE)

        serializer = RoleSerializer(data=request.data, context=request)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                company_id = request.user.profile.company_id
            except:
                return Response({"detail": "User company not selected"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            data["company_id"] = company_id
            data["permissions"] = request.data.get("permissions", "")
            serializer.create(data)
            return Response({"detail": "Role created successfully"}, status=status.HTTP_201_CREATED)


class RoleDetailView(ListAPIView):
    pagination_class = CustomPagination
    permission_classes = (RolePermissions,)

    def get(self, request, pk):
        queryset = Role.objects.filter(pk=pk).first()
        serializer = RoleSerializer(queryset, many=False)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, pk):
        fix_roles = [
            "admin",
            "owner"
        ]
        if request.data.get("name").lower() in fix_roles:
            return Response({"detail": f"User cannot modify role with the name '{request.data.get('name')}'"},
                            status.HTTP_406_NOT_ACCEPTABLE)

        queryset = Role.objects.filter(pk=pk).first()
        serializer = RoleSerializer(queryset, data=request.data)

        if serializer.is_valid():
            serializer.save(permissions=request.data.get("permissions"))
            return Response({"detail": "Role updated successfully"}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        Role.objects.filter(pk=pk).delete()
        return Response({"detail": "Role deleted successfully"}, status=status.HTTP_200_OK)


class RoleUserView(APIView):

    def get(self, request, pk):
        user_profile = request.user.profile
        if user_profile and user_profile.company:
            users = MultipleRoles.objects.filter(role_id=pk).values_list("user_id", flat=True)
            users = User.objects.filter(profile__company=user_profile.company, id__in=users)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"detail": "Current user has no company assign"}, status=status.HTTP_400_BAD_REQUEST)


class AllRoleView(ListAPIView):
    serializer_class = RoleSerializer

    def get_queryset(self):
        return Role.objects.all()
