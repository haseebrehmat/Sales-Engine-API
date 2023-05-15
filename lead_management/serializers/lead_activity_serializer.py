from rest_framework import serializers

from lead_management.models import LeadActivity


class LeadActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadActivity
        fields = '__all__'
