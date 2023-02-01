from rest_framework import serializers
from authentication.models import User


class UserPermissionSerializer(serializers.ModelSerializer):
    # user_permissions = serializers.SerializerMethodField()
    # groups = serializers.SerializerMethodField()
    class Meta:
        model = User
        depth = 3
        exclude = ["password", "is_active", "is_admin", "is_staff", "is_superuser", "last_login"]

    # def get_user_permissions(self, user):
    #     return list(user.get_user_permissions())
    #
    # def get_groups(self, user):
    #     return list(user.get_group_permissions())
