from rest_framework import serializers

from lead_management.models import LeadActivityNotes


class LeadActivityNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadActivityNotes
        fields = '__all__'

