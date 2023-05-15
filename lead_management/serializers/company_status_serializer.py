from rest_framework import serializers

from lead_management.models import CompanyStatus


class CompanyStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyStatus
        fields = '__all__'

