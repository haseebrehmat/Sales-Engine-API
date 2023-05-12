from rest_framework import serializers

from lead_management.models import Phase


class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields = '__all__'
