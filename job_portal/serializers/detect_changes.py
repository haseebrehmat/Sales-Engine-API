from rest_framework import serializers

from authentication.models.company import Company
from job_portal.models import EditHistory
from authentication.models.user import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "code"]

class EditHistorySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    company = CompanySerializer()
    class Meta:
        model = EditHistory
        fields = "__all__"
        depth = 1