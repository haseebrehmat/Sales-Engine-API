from rest_framework import serializers
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # fields = ["id", "username", "email"]
        exclude = ["is_superuser", "password", "last_login", "is_admin", "is_staff", "user_permissions"]
        depth = 1
