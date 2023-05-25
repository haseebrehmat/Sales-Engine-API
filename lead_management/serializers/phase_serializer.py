from rest_framework import serializers

from lead_management.models import Phase
from lead_management.serializers import CompanyStatusSerializer


class PhaseSerializer(serializers.ModelSerializer):
    company_status = CompanyStatusSerializer()

    class Meta:
        model = Phase
        fields = '__all__'


class PhaseNameSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
