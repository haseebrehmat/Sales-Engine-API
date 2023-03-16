from rest_framework import serializers
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()

    class Meta:
        model = User
        # fields = ["id", "username", "email"]
        exclude = ["is_superuser", "password", "last_login", "is_admin", "is_staff", "user_permissions"]
        depth = 1

    def get_company(self, obj):
        try:
            company = obj.profile.company
            company = {
                "id": company.id,
                "name": company.name
            }
        except:
            company = None
        return company
